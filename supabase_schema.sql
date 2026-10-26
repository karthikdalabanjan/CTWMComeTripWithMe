-- ==============================================================================
-- ComeTripWithMe · Supabase PostgreSQL Schema
-- Project: srladqmrbnrkyvjsqywp
-- Run this script in the Supabase SQL Editor:
-- https://supabase.com/dashboard/project/srladqmrbnrkyvjsqywp/sql/new
-- ==============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users & Beta Testers Table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    display_name VARCHAR(100),
    is_beta_tester BOOLEAN DEFAULT TRUE,
    tester_group VARCHAR(50) DEFAULT 'public_beta',
    device_info JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Custom & AI Generated Itineraries
CREATE TABLE IF NOT EXISTS public.custom_itineraries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    session_id VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    duration_days INT NOT NULL,
    vibe VARCHAR(50) NOT NULL,
    budget_tier VARCHAR(20) NOT NULL,
    estimated_price INT NOT NULL,
    day_plans_json JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_custom_itineraries_session ON public.custom_itineraries(session_id);

-- 3. Bookings Table
CREATE TABLE IF NOT EXISTS public.bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_reference VARCHAR(30) UNIQUE NOT NULL,
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    session_id VARCHAR(100) NOT NULL,
    trip_id VARCHAR(50) NOT NULL,
    trip_title VARCHAR(255) NOT NULL,
    tier VARCHAR(20) NOT NULL, -- LUXURY, MID_TIER, BUDGET
    departure_city VARCHAR(100) DEFAULT 'Bengaluru (BLR)',
    travel_date VARCHAR(50) NOT NULL,
    travelers_count INT DEFAULT 1,
    traveler_details_json JSONB NOT NULL,
    base_price NUMERIC(10, 2) NOT NULL,
    discount_amount NUMERIC(10, 2) DEFAULT 0.00,
    voucher_code VARCHAR(50),
    gst_tax NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(30) DEFAULT 'INITIATED', -- INITIATED, PENDING_PAYMENT, CONFIRMED, FAILED, CANCELLED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_bookings_ref ON public.bookings(booking_reference);
CREATE INDEX IF NOT EXISTS idx_bookings_session ON public.bookings(session_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON public.bookings(status);

-- 4. Payments (Razorpay Integration)
CREATE TABLE IF NOT EXISTS public.payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL REFERENCES public.bookings(id) ON DELETE CASCADE,
    razorpay_order_id VARCHAR(100) UNIQUE NOT NULL,
    razorpay_payment_id VARCHAR(100) UNIQUE,
    razorpay_signature VARCHAR(255),
    amount_in_paise BIGINT NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    payment_method VARCHAR(50) DEFAULT 'upi',
    status VARCHAR(30) DEFAULT 'CREATED', -- CREATED, AUTHORIZED, CAPTURED, FAILED
    is_sandbox BOOLEAN DEFAULT TRUE,
    error_code VARCHAR(100),
    error_description TEXT,
    raw_payload_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_payments_order ON public.payments(razorpay_order_id);
CREATE INDEX IF NOT EXISTS idx_payments_payment_id ON public.payments(razorpay_payment_id);

-- 5. Beta Tester Criteria Feedback
CREATE TABLE IF NOT EXISTS public.test_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tester_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    session_id VARCHAR(100) NOT NULL,
    overall_rating INT CHECK (overall_rating BETWEEN 1 AND 5) NOT NULL,
    criteria_scores_json JSONB NOT NULL,
    -- Expected JSON:
    -- { "pricing_accuracy": 5, "audio_guide_experience": 4, "map_waypoint_rendering": 5, "payment_sandbox_flow": 5, "mobile_responsiveness": 5, "offline_and_refresh_state": 4 }
    comments TEXT,
    bug_reports TEXT,
    device_info_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_test_feedback_session ON public.test_feedback(session_id);

-- 6. Telemetry & Funnel Events
CREATE TABLE IF NOT EXISTS public.telemetry_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_payload_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_telemetry_event ON public.telemetry_events(event_name);

-- 7. Wishlist / Saved Trips
CREATE TABLE IF NOT EXISTS public.wishlist_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    trip_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(session_id, trip_id)
);

-- ==============================================================================
-- Row-Level Security (RLS) setup (optional / open for beta testing)
-- ==============================================================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.test_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.custom_itineraries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.telemetry_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wishlist_items ENABLE ROW LEVEL SECURITY;

-- Allow read & write for public API during beta testing
CREATE POLICY "Public read for beta" ON public.bookings FOR SELECT USING (true);
CREATE POLICY "Public insert for beta" ON public.bookings FOR INSERT WITH CHECK (true);
CREATE POLICY "Public update for beta" ON public.bookings FOR UPDATE USING (true);

CREATE POLICY "Public read feedback" ON public.test_feedback FOR SELECT USING (true);
CREATE POLICY "Public insert feedback" ON public.test_feedback FOR INSERT WITH CHECK (true);

CREATE POLICY "Public read itineraries" ON public.custom_itineraries FOR SELECT USING (true);
CREATE POLICY "Public insert itineraries" ON public.custom_itineraries FOR INSERT WITH CHECK (true);

CREATE POLICY "Public read telemetry" ON public.telemetry_events FOR ALL USING (true);
CREATE POLICY "Public read wishlist" ON public.wishlist_items FOR ALL USING (true);
CREATE POLICY "Public read payments" ON public.payments FOR ALL USING (true);
CREATE POLICY "Public read users" ON public.users FOR ALL USING (true);
