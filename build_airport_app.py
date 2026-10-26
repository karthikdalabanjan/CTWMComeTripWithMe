import json

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ComeTripWithMe · India's 1st Creator Tour Operator (Airport & Multi-City Hubs)</title>
    <meta name="description" content="Creator-led curated travel itineraries, airport-mapped destinations, multi-city departure bookings from Bengaluru, Delhi, Mumbai, and live companion pass.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <style>
        :root {
            --bg-dark: #07090E;
            --bg-card: #0F131C;
            --bg-card-elevated: #161C2A;
            --bg-card-hover: #1D2436;
            --gold-primary: #E8C97A;
            --gold-secondary: #D4AF37;
            --gold-light: #FFE8A3;
            --gold-dark: #A68228;
            --gold-glow: rgba(232, 201, 122, 0.28);
            --gold-container: rgba(232, 201, 122, 0.12);
            --glass-border: rgba(232, 201, 122, 0.18);
            --glass-border-strong: rgba(232, 201, 122, 0.38);
            --glass-border-subtle: rgba(255, 255, 255, 0.08);
            --glass-surface: rgba(22, 28, 42, 0.75);
            --text-primary: #F8FAFC;
            --text-secondary: #CBD5E1;
            --text-muted: #94A3B8;
            --text-tertiary: #64748B;
            --accent-green: #3CA082;
            --accent-red: #DC503C;
            --accent-blue: #38BDF8;
            --accent-purple: #A855F7;
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
            --radius-xl: 28px;
            --radius-full: 9999px;
            --shadow-subtle: 0 4px 20px rgba(0, 0, 0, 0.4);
            --shadow-gold: 0 8px 32px rgba(232, 201, 122, 0.15);
            --font-heading: 'Outfit', sans-serif;
            --font-body: 'Plus Jakarta Sans', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: #030407;
            color: var(--text-primary);
            font-family: var(--font-body);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(232, 201, 122, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(56, 189, 248, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(15, 19, 28, 0.85) 0%, #030407 100%);
        }

        .workspace-shell {
            width: 100%;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }

        /* Top Bar Floating Control Switcher */
        .control-pill-bar {
            position: fixed;
            top: 14px;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(15, 19, 28, 0.88);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border-strong);
            padding: 6px 12px;
            border-radius: var(--radius-full);
            box-shadow: 0 10px 30px rgba(0,0,0,0.6), 0 0 15px var(--gold-glow);
            transition: all 0.3s ease;
        }

        .control-btn {
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid transparent;
            padding: 6px 14px;
            border-radius: var(--radius-full);
            font-family: var(--font-heading);
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            letter-spacing: 0.5px;
        }

        .control-btn:hover {
            color: var(--gold-light);
            background: var(--gold-container);
            border-color: var(--glass-border);
        }

        .control-btn.active {
            background: linear-gradient(135deg, var(--gold-primary), var(--gold-secondary));
            color: var(--bg-dark);
            box-shadow: 0 4px 14px rgba(232, 201, 122, 0.4);
        }

        .control-btn.live-pass-btn {
            background: rgba(60, 160, 130, 0.18);
            border-color: rgba(60, 160, 130, 0.45);
            color: #86EFAC;
        }
        .control-btn.live-pass-btn.active {
            background: linear-gradient(135deg, #3CA082, #24755E);
            color: #fff;
            box-shadow: 0 4px 14px rgba(60, 160, 130, 0.4);
        }

        .control-btn.admin-toggle {
            background: rgba(220, 80, 60, 0.15);
            border-color: rgba(220, 80, 60, 0.4);
            color: #FF8F80;
        }
        .control-btn.admin-toggle.active {
            background: linear-gradient(135deg, #DC503C, #B23523);
            color: #fff;
            box-shadow: 0 4px 14px rgba(220, 80, 60, 0.4);
        }

        /* App View Wrapper */
        .app-viewport-wrapper {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 70px 16px 30px;
            min-height: 100vh;
            transition: all 0.4s ease;
        }

        .device-simulator {
            width: 100%;
            max-width: 480px;
            min-height: 880px;
            background: var(--bg-dark);
            border-radius: 46px;
            border: 8px solid #1C2333;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(232, 201, 122, 0.25);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            position: relative;
            transition: max-width 0.4s ease, border-radius 0.4s ease;
        }

        .app-viewport-wrapper.fullscreen-mode .device-simulator {
            max-width: 1200px;
            border-radius: 24px;
            border: 1px solid var(--glass-border);
            min-height: 90vh;
        }

        /* Phone Header Notch */
        .phone-header-notch {
            width: 100%;
            height: 36px;
            background: #06080C;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 22px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            z-index: 50;
        }
        .notch-island {
            width: 110px;
            height: 18px;
            background: #000;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .notch-cam {
            width: 8px;
            height: 8px;
            background: #111;
            border-radius: 50%;
            border: 1px solid #222;
        }

        /* Top Luxury App Header */
        .app-luxury-header {
            position: sticky;
            top: 0;
            z-index: 40;
            background: rgba(7, 9, 14, 0.94);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--glass-border);
            padding: 12px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .brand-cluster {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
        }

        .brand-badge-icon {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, var(--gold-light), var(--gold-secondary) 70%, var(--gold-dark));
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--bg-dark);
            font-size: 20px;
            font-weight: 900;
            box-shadow: 0 4px 15px var(--gold-glow);
            transition: transform 0.3s ease;
        }
        .brand-cluster:hover .brand-badge-icon {
            transform: rotate(45deg) scale(1.05);
        }

        .brand-text-col {
            display: flex;
            flex-direction: column;
        }
        .brand-title {
            font-family: var(--font-heading);
            font-size: 16px;
            font-weight: 900;
            letter-spacing: 1.8px;
            background: linear-gradient(135deg, #FFF, var(--gold-primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }
        .brand-subtitle {
            font-size: 9px;
            font-weight: 600;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            text-transform: uppercase;
        }

        .header-action-row {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Departure Origin City Switcher Bar */
        .origin-hub-selector-bar {
            background: linear-gradient(90deg, #111726, #0D1322);
            border-bottom: 1px solid var(--glass-border);
            padding: 8px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            gap: 8px;
        }
        .origin-pills-group {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .origin-city-btn {
            background: var(--bg-card);
            border: 1px solid var(--glass-border-subtle);
            color: var(--text-secondary);
            font-family: var(--font-heading);
            font-size: 11px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: var(--radius-full);
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .origin-city-btn:hover {
            border-color: var(--gold-primary);
            color: var(--gold-light);
        }
        .origin-city-btn.active {
            background: linear-gradient(135deg, var(--gold-primary), var(--gold-secondary));
            color: var(--bg-dark);
            border-color: var(--gold-primary);
            box-shadow: 0 2px 8px rgba(232, 201, 122, 0.4);
        }

        .icon-circle-btn {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--glass-surface);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }
        .icon-circle-btn:hover {
            transform: translateY(-2px);
            border-color: var(--gold-primary);
            background: var(--gold-container);
            color: var(--gold-light);
        }
        .icon-circle-btn.whatsapp-accent {
            background: rgba(60, 160, 130, 0.15);
            border-color: rgba(60, 160, 130, 0.4);
            color: #4ADE80;
        }

        /* Scrollable Body */
        .app-content-body {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding-bottom: 90px;
            scrollbar-width: thin;
            scrollbar-color: var(--gold-dark) var(--bg-dark);
        }
        .app-content-body::-webkit-scrollbar {
            width: 6px;
        }
        .app-content-body::-webkit-scrollbar-thumb {
            background: var(--glass-border-strong);
            border-radius: 10px;
        }

        /* Bottom Luxury Navbar */
        .app-bottom-navbar {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 45;
            background: rgba(15, 19, 28, 0.95);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-top: 1px solid var(--glass-border);
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 8px 6px 14px;
            border-top-left-radius: 24px;
            border-top-right-radius: 24px;
        }

        .nav-item-btn {
            background: transparent;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: var(--text-muted);
            font-size: 10px;
            font-weight: 600;
            cursor: pointer;
            padding: 6px 10px;
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
            position: relative;
        }
        .nav-item-btn i {
            font-size: 18px;
            transition: transform 0.2s ease;
        }
        .nav-item-btn:hover {
            color: var(--text-secondary);
        }
        .nav-item-btn.active {
            color: var(--gold-primary);
        }
        .nav-item-btn.active i {
            transform: scale(1.15) translateY(-2px);
            filter: drop-shadow(0 0 8px var(--gold-glow));
        }
        .nav-item-btn.active::after {
            content: '';
            position: absolute;
            bottom: 0px;
            width: 16px;
            height: 3px;
            background: var(--gold-primary);
            border-radius: 3px;
            box-shadow: 0 0 8px var(--gold-primary);
        }

        /* Screens */
        .screen-view {
            display: none;
            opacity: 0;
            transform: translateY(8px);
            transition: opacity 0.3s ease, transform 0.3s ease;
            padding: 18px;
        }
        .screen-view.active-screen {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        /* Luxury Components */
        .glass-panel {
            background: var(--glass-surface);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 18px;
            box-shadow: var(--shadow-subtle);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            margin-bottom: 18px;
            position: relative;
            overflow: hidden;
        }

        .gold-btn {
            background: linear-gradient(135deg, var(--gold-primary) 0%, var(--gold-secondary) 100%);
            color: var(--bg-dark);
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 800;
            border: none;
            padding: 12px 20px;
            border-radius: var(--radius-full);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 18px rgba(232, 201, 122, 0.35);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            letter-spacing: 0.4px;
        }
        .gold-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(232, 201, 122, 0.55);
            filter: brightness(1.08);
        }

        .glass-btn {
            background: var(--glass-surface);
            color: var(--text-primary);
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 700;
            border: 1px solid var(--glass-border);
            padding: 12px 18px;
            border-radius: var(--radius-full);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s ease;
            text-decoration: none;
        }
        .glass-btn:hover {
            background: var(--gold-container);
            border-color: var(--gold-primary);
            color: var(--gold-light);
            transform: translateY(-2px);
        }

        .gold-badge {
            background: var(--gold-container);
            border: 1px solid var(--glass-border-strong);
            color: var(--gold-light);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: var(--radius-full);
            display: inline-flex;
            align-items: center;
            gap: 5px;
            letter-spacing: 0.3px;
        }

        .airport-hub-badge {
            background: rgba(56, 189, 248, 0.18);
            border: 1px solid rgba(56, 189, 248, 0.45);
            color: #7DD3FC;
            font-size: 11px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: var(--radius-full);
            display: inline-flex;
            align-items: center;
            gap: 5px;
            letter-spacing: 0.4px;
        }

        .vibe-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: var(--radius-full);
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .vibe-party { background: rgba(220, 80, 60, 0.2); color: #FFA090; border: 1px solid rgba(220, 80, 60, 0.4); }
        .vibe-backpacking { background: rgba(56, 189, 248, 0.2); color: #BAE6FD; border: 1px solid rgba(56, 189, 248, 0.4); }
        .vibe-chill { background: rgba(60, 160, 130, 0.2); color: #86EFAC; border: 1px solid rgba(60, 160, 130, 0.4); }
        .vibe-luxury { background: rgba(232, 201, 122, 0.2); color: var(--gold-light); border: 1px solid var(--glass-border-strong); }
        .vibe-heritage { background: rgba(179, 125, 78, 0.2); color: #FCD34D; border: 1px solid rgba(179, 125, 78, 0.4); }

        .section-title-wrap {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 14px;
        }
        .section-title {
            font-family: var(--font-heading);
            font-size: 18px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-title span.sparkle {
            color: var(--gold-primary);
        }
        .section-subtitle {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        /* Hero Banner */
        .hero-banner-card {
            background: linear-gradient(180deg, rgba(15, 19, 28, 0.4) 0%, rgba(7, 9, 14, 0.95) 100%),
                        url('https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=1200&q=80') center/cover no-repeat;
            border-radius: var(--radius-xl);
            border: 1px solid var(--glass-border-strong);
            padding: 24px 20px;
            margin-bottom: 22px;
            position: relative;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7);
        }
        .hero-banner-content {
            position: relative;
            z-index: 2;
        }
        .hero-title {
            font-family: var(--font-heading);
            font-size: 24px;
            font-weight: 900;
            line-height: 1.2;
            margin: 10px 0 8px;
            background: linear-gradient(135deg, #FFFFFF, var(--gold-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-desc {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 16px;
        }

        /* Filter Chips Horizontal Scroller */
        .scroll-chips-row {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 10px;
            scrollbar-width: none;
            margin-bottom: 16px;
        }
        .scroll-chips-row::-webkit-scrollbar {
            display: none;
        }
        .filter-chip {
            background: var(--glass-surface);
            border: 1px solid var(--glass-border);
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: var(--radius-full);
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .filter-chip:hover {
            border-color: var(--gold-primary);
            color: var(--gold-light);
        }
        .filter-chip.active {
            background: linear-gradient(135deg, var(--gold-primary), var(--gold-secondary));
            color: var(--bg-dark);
            border-color: var(--gold-primary);
            font-weight: 800;
            box-shadow: 0 4px 14px rgba(232, 201, 122, 0.3);
        }

        /* Spotlights Carousel */
        .spotlights-carousel {
            display: flex;
            gap: 12px;
            overflow-x: auto;
            padding-bottom: 10px;
            scrollbar-width: none;
            margin-bottom: 22px;
        }
        .spotlight-card {
            min-width: 240px;
            height: 140px;
            border-radius: var(--radius-lg);
            border: 1px solid var(--glass-border);
            position: relative;
            overflow: hidden;
            flex-shrink: 0;
            cursor: pointer;
            box-shadow: var(--shadow-subtle);
            transition: transform 0.25s ease;
        }
        .spotlight-card:hover {
            transform: translateY(-4px);
            border-color: var(--gold-primary);
        }
        .spotlight-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .spotlight-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(7,9,14,0.9) 100%);
            padding: 14px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        .spotlight-region {
            font-size: 9px;
            color: var(--gold-primary);
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }
        .spotlight-name {
            font-family: var(--font-heading);
            font-size: 15px;
            font-weight: 800;
            color: #fff;
        }

        /* Trips Grid */
        .trips-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 18px;
            margin-bottom: 24px;
        }
        @media (min-width: 768px) {
            .app-viewport-wrapper.fullscreen-mode .trips-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (min-width: 1024px) {
            .app-viewport-wrapper.fullscreen-mode .trips-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        .trip-card {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            position: relative;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            box-shadow: var(--shadow-subtle);
        }
        .trip-card:hover {
            transform: translateY(-4px);
            border-color: var(--gold-primary);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px var(--gold-glow);
        }

        .trip-card-image-wrap {
            width: 100%;
            height: 180px;
            position: relative;
            overflow: hidden;
        }
        .trip-card-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        .trip-card:hover .trip-card-image {
            transform: scale(1.06);
        }

        .trip-card-overlay-top {
            position: absolute;
            top: 12px;
            left: 12px;
            right: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .wishlist-heart-btn {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: rgba(15, 19, 28, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        .wishlist-heart-btn:hover {
            transform: scale(1.1);
        }
        .wishlist-heart-btn.is-saved {
            color: #FF5A5F;
            border-color: #FF5A5F;
            background: rgba(255, 90, 95, 0.2);
        }

        .trip-card-overlay-bottom {
            position: absolute;
            bottom: 10px;
            left: 12px;
            right: 12px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .trip-price-pill {
            background: rgba(7, 9, 14, 0.88);
            border: 1px solid var(--glass-border-strong);
            padding: 4px 10px;
            border-radius: var(--radius-full);
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 800;
            color: var(--gold-light);
        }
        .trip-duration-pill {
            background: rgba(7, 9, 14, 0.88);
            border: 1px solid var(--glass-border-subtle);
            padding: 4px 10px;
            border-radius: var(--radius-full);
            font-size: 11px;
            font-weight: 600;
            color: var(--text-secondary);
        }

        .trip-card-body {
            padding: 16px;
        }
        .trip-card-title {
            font-family: var(--font-heading);
            font-size: 17px;
            font-weight: 800;
            color: #fff;
            margin-bottom: 4px;
        }
        .trip-card-headline {
            font-size: 12px;
            color: var(--gold-light);
            font-weight: 600;
            margin-bottom: 8px;
        }

        .trip-card-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 14px;
        }
        .tag-pill {
            background: var(--bg-card-elevated);
            border: 1px solid var(--glass-border-subtle);
            color: var(--text-secondary);
            font-size: 10px;
            padding: 3px 8px;
            border-radius: var(--radius-full);
        }

        .trip-card-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid var(--glass-border-subtle);
            padding-top: 12px;
        }

        /* Transit & Stay Cards in Timeline */
        .transit-hub-card {
            background: linear-gradient(145deg, rgba(15, 25, 45, 0.85), rgba(7, 12, 20, 0.95));
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: var(--radius-lg);
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5), 0 0 15px rgba(56, 189, 248, 0.15);
            position: relative;
        }
        .transit-hub-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 16px;
            bottom: 16px;
            width: 4px;
            background: var(--accent-blue);
            border-radius: 0 4px 4px 0;
        }

        .hotel-hub-card {
            background: linear-gradient(145deg, rgba(28, 18, 42, 0.85), rgba(12, 8, 20, 0.95));
            border: 1px solid rgba(168, 85, 247, 0.35);
            border-radius: var(--radius-lg);
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5), 0 0 15px rgba(168, 85, 247, 0.15);
            position: relative;
        }
        .hotel-hub-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 16px;
            bottom: 16px;
            width: 4px;
            background: var(--accent-purple);
            border-radius: 0 4px 4px 0;
        }

        .inter-stop-transit-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(15, 19, 28, 0.7);
            border: 1px dashed var(--glass-border);
            padding: 4px 10px;
            border-radius: var(--radius-full);
            font-size: 10px;
            font-weight: 700;
            color: var(--gold-light);
            margin: 6px 0 14px 14px;
        }

        /* Digital Boarding Pass Ticket */
        .boarding-pass-card {
            background: #10141F;
            border: 1px solid var(--gold-primary);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 0 0 30px var(--gold-glow);
            margin-bottom: 20px;
            position: relative;
        }
        .boarding-pass-header {
            background: linear-gradient(135deg, var(--gold-primary), var(--gold-secondary));
            color: #07090E;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .boarding-pass-body {
            padding: 20px;
        }
        .ticket-perforated-divider {
            position: relative;
            border-top: 2px dashed rgba(232, 201, 122, 0.3);
            margin: 16px 0;
        }
        .ticket-perforated-divider::before {
            content: '';
            position: absolute;
            left: -30px;
            top: -12px;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #030407;
        }
        .ticket-perforated-divider::after {
            content: '';
            position: absolute;
            right: -30px;
            top: -12px;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #030407;
        }

        .ticket-meta-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        .ticket-label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            margin-bottom: 2px;
        }
        .ticket-val {
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 800;
            color: #fff;
        }
        .ticket-val.mono {
            font-family: var(--font-mono);
            color: var(--gold-light);
        }

        /* Live Companion Time-Traveler Simulator HUD */
        .time-traveler-hud {
            background: linear-gradient(145deg, #131926, #090D15);
            border: 1px solid var(--gold-primary);
            border-radius: var(--radius-lg);
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6), 0 0 20px var(--gold-glow);
        }
        .live-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(60, 160, 130, 0.2);
            border: 1px solid var(--accent-green);
            color: #86EFAC;
            font-size: 11px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: var(--radius-full);
        }

        /* Route Map Interactive Visualizer */
        .route-map-box {
            width: 100%;
            height: 240px;
            background: #090C12;
            border-radius: var(--radius-lg);
            border: 1px solid var(--glass-border);
            position: relative;
            overflow: hidden;
            margin-bottom: 18px;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.8);
        }
        .map-svg-canvas {
            width: 100%;
            height: 100%;
        }
        .map-info-badge {
            position: absolute;
            bottom: 10px;
            left: 12px;
            background: rgba(7, 9, 14, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            padding: 6px 12px;
            border-radius: var(--radius-full);
            font-size: 10px;
            font-weight: 700;
            color: var(--gold-light);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Stops List & Stop Cards */
        .stops-timeline {
            position: relative;
            padding-left: 24px;
            margin-bottom: 24px;
        }
        .stops-timeline::before {
            content: '';
            position: absolute;
            top: 15px;
            bottom: 15px;
            left: 8px;
            width: 2px;
            background: linear-gradient(180deg, var(--gold-primary) 0%, rgba(232, 201, 122, 0.1) 100%);
        }

        .stop-timeline-item {
            position: relative;
            margin-bottom: 20px;
        }
        .stop-dot-marker {
            position: absolute;
            left: -24px;
            top: 16px;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--bg-dark);
            border: 2px solid var(--gold-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            color: var(--gold-primary);
            box-shadow: 0 0 10px var(--gold-glow);
            z-index: 2;
        }
        .stop-dot-marker.visited {
            background: var(--accent-green);
            border-color: var(--accent-green);
            color: #fff;
        }

        .stop-card {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            padding: 16px;
            transition: all 0.25s ease;
        }
        .stop-card:hover {
            border-color: var(--gold-primary);
            transform: translateX(4px);
        }

        .stop-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        .stop-name {
            font-family: var(--font-heading);
            font-size: 15px;
            font-weight: 800;
            color: #fff;
        }
        .stop-time-badge {
            font-size: 11px;
            font-weight: 700;
            color: var(--gold-light);
            background: var(--gold-container);
            padding: 2px 8px;
            border-radius: var(--radius-full);
            border: 1px solid var(--glass-border);
        }

        .stop-img-preview {
            width: 100%;
            height: 130px;
            border-radius: var(--radius-md);
            object-fit: cover;
            margin: 10px 0;
            border: 1px solid var(--glass-border-subtle);
        }

        .insider-tip-box {
            background: rgba(232, 201, 122, 0.07);
            border-left: 3px solid var(--gold-primary);
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 11px;
            color: var(--text-secondary);
            margin: 10px 0;
            line-height: 1.4;
        }
        .insider-tip-box strong {
            color: var(--gold-light);
        }

        .stop-actions-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px solid var(--glass-border-subtle);
        }

        /* Audio Player Bar */
        .live-audio-player-bar {
            position: fixed;
            bottom: 74px;
            left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 32px);
            max-width: 440px;
            background: rgba(22, 28, 42, 0.95);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--gold-primary);
            border-radius: var(--radius-lg);
            padding: 12px 16px;
            display: none;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px var(--gold-glow);
            z-index: 48;
            animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        @keyframes slideUp {
            from { transform: translate(-50%, 20px); opacity: 0; }
            to { transform: translate(-50%, 0); opacity: 1; }
        }
        .app-viewport-wrapper.fullscreen-mode .live-audio-player-bar {
            max-width: 600px;
        }

        .audio-player-left {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            flex: 1;
            overflow: hidden;
        }
        .audio-wave-anim {
            display: flex;
            align-items: flex-end;
            gap: 3px;
            height: 20px;
        }
        .wave-bar {
            width: 3px;
            background: var(--gold-primary);
            border-radius: 2px;
            height: 6px;
            animation: waveBounce 1.2s infinite ease-in-out;
        }
        .wave-bar:nth-child(2) { animation-delay: 0.2s; }
        .wave-bar:nth-child(3) { animation-delay: 0.4s; }
        .wave-bar:nth-child(4) { animation-delay: 0.6s; }
        @keyframes waveBounce {
            0%, 100% { height: 6px; }
            50% { height: 20px; }
        }
        .audio-wave-anim.paused .wave-bar {
            animation: none;
            height: 6px;
        }

        .audio-title-wrap {
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
        .audio-story-title {
            font-family: var(--font-heading);
            font-size: 13px;
            font-weight: 800;
            color: #fff;
        }
        .audio-narrator {
            font-size: 10px;
            color: var(--gold-primary);
        }

        .audio-player-controls {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .audio-play-btn {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: var(--gold-primary);
            color: var(--bg-dark);
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 0 15px var(--gold-glow);
            transition: transform 0.2s ease;
        }
        .audio-play-btn:hover {
            transform: scale(1.1);
        }

        /* Video Proofs & Reels */
        .video-proof-card {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            margin-bottom: 18px;
            transition: all 0.3s ease;
        }
        .video-thumb-wrap {
            width: 100%;
            height: 180px;
            position: relative;
            cursor: pointer;
        }
        .video-thumb-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .video-play-overlay {
            position: absolute;
            inset: 0;
            background: rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .youtube-play-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(220, 80, 60, 0.9);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 0 20px rgba(220, 80, 60, 0.6);
        }

        .reels-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 22px;
        }
        .reel-card {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            position: relative;
            cursor: pointer;
        }
        .reel-card-img {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        .reel-card-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(7,9,14,0.95) 100%);
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* Packing List */
        .packing-item-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--bg-card);
            border: 1px solid var(--glass-border-subtle);
            border-radius: var(--radius-md);
            padding: 10px 14px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }
        .packing-item-row.checked {
            opacity: 0.6;
            text-decoration: line-through;
            border-color: rgba(60, 160, 130, 0.4);
        }
        .custom-checkbox {
            width: 20px;
            height: 20px;
            border-radius: 6px;
            border: 1.5px solid var(--glass-border-strong);
            background: transparent;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: transparent;
            font-size: 12px;
        }
        .packing-item-row.checked .custom-checkbox {
            background: var(--accent-green);
            border-color: var(--accent-green);
            color: #fff;
        }

        /* Modals */
        .modal-backdrop {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            z-index: 2000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
            animation: fadeIn 0.2s ease;
        }
        .modal-backdrop.open {
            display: flex;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-dialog {
            width: 100%;
            max-width: 620px;
            max-height: 90vh;
            background: var(--bg-card);
            border: 1px solid var(--glass-border-strong);
            border-radius: var(--radius-xl);
            box-shadow: 0 25px 80px rgba(0,0,0,0.9), 0 0 30px var(--gold-glow);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            animation: scaleUp 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        @keyframes scaleUp {
            from { transform: scale(0.92); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .modal-header {
            padding: 18px 22px;
            border-bottom: 1px solid var(--glass-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-card-elevated);
        }
        .modal-title {
            font-family: var(--font-heading);
            font-size: 18px;
            font-weight: 800;
            color: #fff;
        }
        .modal-close-btn {
            background: var(--glass-surface);
            border: 1px solid var(--glass-border);
            color: var(--text-muted);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        .modal-close-btn:hover {
            color: #fff;
            border-color: var(--gold-primary);
        }

        .modal-body {
            padding: 22px;
            overflow-y: auto;
            flex: 1;
        }
        .modal-footer {
            padding: 16px 22px;
            border-top: 1px solid var(--glass-border);
            background: var(--bg-card-elevated);
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }

        /* CMS Drawer Panel */
        .cms-drawer-panel {
            position: fixed;
            top: 0;
            right: -100%;
            width: 100%;
            max-width: 540px;
            height: 100vh;
            background: #090C13;
            border-left: 1px solid var(--glass-border-strong);
            box-shadow: -10px 0 40px rgba(0,0,0,0.8);
            z-index: 3000;
            transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
        }
        .cms-drawer-panel.open {
            right: 0;
        }

        .cms-header {
            padding: 18px 20px;
            background: #111622;
            border-bottom: 1px solid var(--glass-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .cms-body {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        .cms-tabs-row {
            display: flex;
            gap: 6px;
            border-bottom: 1px solid var(--glass-border);
            padding-bottom: 10px;
            margin-bottom: 18px;
            overflow-x: auto;
        }
        .cms-tab-btn {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: var(--radius-md);
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
        }
        .cms-tab-btn.active {
            background: var(--gold-container);
            border-color: var(--glass-border-strong);
            color: var(--gold-light);
        }

        /* Toast Container */
        .toast-container {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 5000;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .toast-msg {
            background: rgba(22, 28, 42, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid var(--gold-primary);
            border-radius: var(--radius-md);
            padding: 12px 18px;
            color: #fff;
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px var(--gold-glow);
            animation: slideInRight 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        @keyframes slideInRight {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .app-footer-box {
            padding: 24px 18px;
            border-top: 1px solid var(--glass-border);
            background: var(--bg-dark);
            margin-top: 30px;
            border-radius: var(--radius-lg);
        }
        .footer-brand {
            font-family: var(--font-heading);
            font-size: 18px;
            font-weight: 900;
            color: var(--gold-primary);
            letter-spacing: 1.5px;
            margin-bottom: 6px;
        }
        .footer-social-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 16px 0;
        }
    </style>
</head>
<body>

<div class="workspace-shell">

    <!-- Top Floating Master Bar -->
    <div class="control-pill-bar">
        <button class="control-btn active" id="btnViewMobile" onclick="toggleViewportMode('mobile')">
            <i class="fa-solid fa-mobile-screen"></i> Mobile App
        </button>
        <button class="control-btn" id="btnViewDesktop" onclick="toggleViewportMode('desktop')">
            <i class="fa-solid fa-desktop"></i> Desktop View
        </button>
        <button class="control-btn live-pass-btn" id="btnLivePass" onclick="openActiveBoardingPassModal()">
            <i class="fa-solid fa-ticket"></i> Live Pass & HUD
        </button>
        <button class="control-btn admin-toggle" id="btnCmsTrigger" onclick="toggleCmsDrawer()">
            <i class="fa-solid fa-sliders"></i> Master Controller
        </button>
    </div>

    <!-- Main Viewport Wrapper -->
    <div class="app-viewport-wrapper" id="viewportWrapper">
        <div class="device-simulator" id="deviceSimulator">
            
            <!-- Phone Notch -->
            <div class="phone-header-notch" id="phoneNotch">
                <span id="liveClock">9:41</span>
                <div class="notch-island"><div class="notch-cam"></div></div>
                <div style="display:flex; gap:6px; align-items:center;">
                    <i class="fa-solid fa-signal" style="font-size:10px;"></i>
                    <i class="fa-solid fa-wifi" style="font-size:10px;"></i>
                    <i class="fa-solid fa-battery-full" style="font-size:11px;"></i>
                </div>
            </div>

            <!-- Top Luxury Header -->
            <header class="app-luxury-header">
                <div class="brand-cluster" onclick="switchTab('explore')">
                    <div class="brand-badge-icon">✦</div>
                    <div class="brand-text-col">
                        <span class="brand-title" id="appBrandTitle">COMETRIPWITHME</span>
                        <span class="brand-subtitle" id="appBrandSubtitle">India's 1st Creator Tour Operator</span>
                    </div>
                </div>
                <div class="header-action-row">
                    <button class="icon-circle-btn" onclick="openInstagramChannel('@cometriipwme')" title="Instagram">
                        <i class="fa-brands fa-instagram"></i>
                    </button>
                    <button class="icon-circle-btn whatsapp-accent" onclick="openWhatsAppInquiry()" title="WhatsApp Inquiry">
                        <i class="fa-brands fa-whatsapp"></i>
                    </button>
                </div>
            </header>

            <!-- Global Departure Origin Selector (BLR / DEL / BOM) -->
            <div class="origin-hub-selector-bar">
                <span style="font-weight:800; color:var(--gold-light); display:flex; align-items:center; gap:5px;">
                    <i class="fa-solid fa-plane-departure" style="color:var(--accent-blue);"></i> Flying From:
                </span>
                <div class="origin-pills-group" id="originCityPillsGroup">
                    <button class="origin-city-btn active" id="originBtn-BLR" onclick="setGlobalOriginCity('BLR')">
                        <span>BLR</span> · Bengaluru
                    </button>
                    <button class="origin-city-btn" id="originBtn-DEL" onclick="setGlobalOriginCity('DEL')">
                        <span>DEL</span> · Delhi
                    </button>
                    <button class="origin-city-btn" id="originBtn-BOM" onclick="setGlobalOriginCity('BOM')">
                        <span>BOM</span> · Mumbai
                    </button>
                </div>
            </div>

            <!-- Scrollable Body -->
            <main class="app-content-body" id="appMainScroll">

                <!-- ================= TAB 1: EXPLORE (AIRPORT RESTRUCTURED) ================= -->
                <section class="screen-view active-screen" id="screen-explore">
                    
                    <!-- Hero Banner -->
                    <div class="hero-banner-card">
                        <div class="hero-banner-content">
                            <span class="gold-badge" id="heroOriginTag">✦ DEPARTING FROM BENGALURU (BLR) · AIRPORT MAPPED</span>
                            <h1 class="hero-title">Creator Travel Restructured by Direct Airport Hubs</h1>
                            <p class="hero-desc">Choose departure from Bengaluru, Delhi, or Mumbai. Get direct airport boarding gates, arrival baggage belts, pre-assigned resort cabs, and live GPS pins.</p>
                            <div style="display:flex; gap:10px; flex-wrap:wrap;">
                                <button class="gold-btn" onclick="openActiveBoardingPassModal()">
                                    <i class="fa-solid fa-ticket"></i> Live Booking Pass ✦
                                </button>
                                <button class="glass-btn" onclick="switchTab('planner')">
                                    <i class="fa-solid fa-compass"></i> Custom Route Builder
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Destination Spotlights by Airport Gateway -->
                    <div class="section-title-wrap">
                        <div>
                            <h2 class="section-title"><span class="sparkle">✦</span> Airport Gateways & Spotlights</h2>
                            <p class="section-subtitle">Direct flight connections from <span id="spotlightOriginName" style="color:var(--gold-light); font-weight:700;">Bengaluru (BLR)</span></p>
                        </div>
                    </div>
                    <div class="spotlights-carousel" id="spotlightsContainer"></div>

                    <!-- Airport Hub Filter Chips -->
                    <div class="section-title-wrap">
                        <div>
                            <h2 class="section-title"><span class="sparkle">✦</span> Curated Destination Airports</h2>
                            <p class="section-subtitle">Filter by landing airport code & route</p>
                        </div>
                    </div>
                    <div class="scroll-chips-row" id="airportFilterChips">
                        <button class="filter-chip active" onclick="filterTripsByAirport('ALL', this)">All Airport Hubs</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('GOX', this)">🏖️ GOX · Goa Mopa</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('BKK', this)">🏝️ BKK · Bangkok</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('KBV', this)">🌊 KBV · Krabi</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('KUU', this)">🏔️ KUU · Kullu-Manali</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('KLIA', this)">🏙️ KLIA · Malaysia</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('MAA', this)">🏛️ MAA · Pondicherry/Chennai</button>
                        <button class="filter-chip" onclick="filterTripsByAirport('HBX', this)">🌴 HBX · Gokarna/Hubballi</button>
                    </div>

                    <!-- Trips Grid -->
                    <div class="trips-grid" id="tripsGridContainer"></div>

                    <!-- Smart Match Trip Recommender Box -->
                    <div class="smart-match-box">
                        <div class="section-title-wrap" style="margin-bottom:6px;">
                            <div>
                                <span class="gold-badge" style="margin-bottom:6px;">✦ AI SMART MATCH</span>
                                <h3 class="section-title">Instant Flight & Trip Matcher</h3>
                            </div>
                        </div>
                        <p style="font-size:12px; color:var(--text-secondary); margin-bottom:14px;">Find the exact itinerary matched to your departure airport, squad, and budget.</p>

                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                            <div class="match-field-group">
                                <label class="match-field-label">Departure Airport (From)</label>
                                <select class="match-input-select" id="smartOriginSelect" onchange="setGlobalOriginCity(this.value)">
                                    <option value="BLR">BLR · Bengaluru (Kempegowda T2)</option>
                                    <option value="DEL">DEL · Delhi (Indira Gandhi T3)</option>
                                    <option value="BOM">BOM · Mumbai (CSMIA T2)</option>
                                </select>
                            </div>
                            <div class="match-field-group">
                                <label class="match-field-label">Destination Airport (To)</label>
                                <select class="match-input-select" id="smartDestSelect" onchange="runSmartMatch()">
                                    <option value="goa">GOX · Goa Mopa Airport</option>
                                    <option value="thailand">BKK · Bangkok Suvarnabhumi</option>
                                    <option value="himachal">KUU · Kullu-Manali Bhuntar</option>
                                    <option value="gokarna">HBX/GOI · Gokarna Gateway</option>
                                    <option value="pondicherry">MAA/PNY · Pondicherry / Chennai</option>
                                    <option value="malaysia">KLIA · Kuala Lumpur</option>
                                    <option value="krabi">KBV · Krabi Islands</option>
                                </select>
                            </div>
                        </div>

                        <div class="match-field-group">
                            <label class="match-field-label">Max Budget Per Person</label>
                            <div class="budget-slider-row">
                                <input type="range" class="budget-slider" id="smartBudgetSlider" min="3000" max="45000" step="1000" value="15000" oninput="updateBudgetSliderVal(this.value)">
                                <span class="budget-display-val" id="smartBudgetVal">₹15,000</span>
                            </div>
                        </div>

                        <div class="smart-result-card" id="smartResultCard">
                            <span class="smart-result-title" id="smartResultTitle">✦ Full Goa Circuit — ₹8,999/person</span>
                            <p class="smart-result-sub" id="smartResultSub">4 nights, North + South Goa blend. Thalassa sunset, Chapora cliff views, and pristine Palolem silence.</p>
                            <div style="margin-top:8px; display:flex; gap:8px;">
                                <button class="gold-btn" style="padding:8px 16px; font-size:11px;" onclick="viewSmartMatchedTrip()">
                                    View Recommended Flight & Trip ✦
                                </button>
                                <button class="glass-btn" style="padding:8px 16px; font-size:11px;" onclick="inquireSmartMatchWhatsApp()">
                                    Inquire on WhatsApp 💬
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="app-footer-box">
                        <div class="footer-brand" id="footerBrandName">COMETRIPWITHME</div>
                        <p style="font-size:12px; color:var(--text-secondary); line-height:1.5;">India's first creator-led tour operator. Direct airport routes, real places — curated with verified route proof. Based in Bengaluru, Delhi & Mumbai ☕.</p>
                        
                        <div style="background:var(--bg-card); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:12px; margin:14px 0;">
                            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                                <span style="font-size:12px; color:var(--text-primary);"><i class="fa-solid fa-phone" style="color:var(--gold-primary); margin-right:6px;"></i> +91 97423 11023</span>
                                <a href="tel:+919742311023" class="gold-badge" style="text-decoration:none;">Call 📞</a>
                            </div>
                            <div style="display:flex; align-items:center; justify-content:space-between;">
                                <span style="font-size:12px; color:var(--text-primary);"><i class="fa-solid fa-envelope" style="color:var(--gold-primary); margin-right:6px;"></i> bengalurufoodss@gmail.com</span>
                                <a href="mailto:bengalurufoodss@gmail.com" class="gold-badge" style="text-decoration:none;">Email ✉️</a>
                            </div>
                        </div>

                        <div class="footer-social-chips">
                            <span class="gold-badge" onclick="openInstagramChannel('@cometriipwme')" style="cursor:pointer;">📸 @cometriipwme</span>
                            <span class="gold-badge" onclick="openInstagramChannel('@beyondbengalurufoods')" style="cursor:pointer;">🍜 @beyondbengalurufoods</span>
                            <span class="gold-badge" onclick="openYouTubeChannel()" style="cursor:pointer;">▶ YouTube</span>
                            <span class="gold-badge" onclick="openWhatsAppInquiry()" style="cursor:pointer;">💬 WhatsApp</span>
                        </div>
                        <p style="font-size:10px; color:var(--text-tertiary);">© 2025 ComeTripWithMe · Handcrafted in Bengaluru</p>
                    </div>

                </section>

                <!-- ================= TAB 2: POCKET GUIDE & REAL-TIME LOGISTICS ================= -->
                <section class="screen-view" id="screen-guide">
                    
                    <!-- Guide Header & Trip Switcher -->
                    <div class="guide-active-trip-selector">
                        <div>
                            <span style="font-size:10px; color:var(--gold-primary); font-weight:700; text-transform:uppercase;">Active Pocket Guide</span>
                            <h3 style="font-family:var(--font-heading); font-size:16px; font-weight:800; color:#fff;" id="guideActiveTripTitle">Goa Long Weekend</h3>
                        </div>
                        <select class="match-input-select" style="width:auto; padding:6px 12px; font-size:11px;" id="guideTripDropdown" onchange="switchGuideTrip(this.value)">
                            <!-- Populated via JS -->
                        </select>
                    </div>

                    <!-- Real-Time Time-Traveler Live Status HUD -->
                    <div class="time-traveler-hud">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span class="live-status-pill" id="hudLivePill">🟢 LIVE · FLIGHT BOARDING IN 40 MINS</span>
                            <span style="font-family:var(--font-mono); font-size:11px; color:var(--gold-light);" id="hudSimTime">06:00 AM</span>
                        </div>
                        <div style="font-size:13px; font-weight:800; color:#fff; margin-bottom:4px;" id="hudStageTitle">
                            ✈️ BLR T2 ➔ GOX · Flight 6E-204
                        </div>
                        <p style="font-size:11px; color:var(--text-secondary); line-height:1.4; margin-bottom:12px;" id="hudStageDesc">
                            Gate 14B boarding starts in 40 mins. Pre-flight filter coffee at Hatti Kaapi Gate 12.
                        </p>

                        <!-- Draggable Time-Traveler Slider -->
                        <div style="margin-top:10px;">
                            <div style="display:flex; justify-content:space-between; font-size:10px; color:var(--text-muted); margin-bottom:4px;">
                                <span>T-3h Airport</span>
                                <span>🚖 Cab Pickup</span>
                                <span>🏨 Resort Arrival</span>
                                <span>🌅 Evening Spot</span>
                            </div>
                            <input type="range" class="budget-slider" id="timelineSlider" min="0" max="4" step="1" value="0" oninput="scrubTimelineStage(this.value)">
                        </div>
                    </div>

                    <!-- Real-Time Transit Logistics Hub (Airport, Cab, Hotel) -->
                    <div id="guideTransitHubSection"></div>

                    <!-- Day Tabs -->
                    <div class="guide-day-tabs" id="guideDayTabsContainer"></div>

                    <!-- Day Summary & Live Progress -->
                    <div class="glass-panel" style="padding:14px; margin-bottom:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="font-size:12px; font-weight:700; color:var(--gold-light);" id="guideDayTitle">Day 1: North Goa Cliff Discovery</span>
                            <span style="font-size:11px; color:var(--text-muted);" id="guideProgressCounter">0 / 3 Visited</span>
                        </div>
                        <p style="font-size:11px; color:var(--text-secondary); line-height:1.4; margin-bottom:10px;" id="guideDaySummary">
                            Sunrise scooter crawl, Chapora cliff panoramas, hidden Anjuna ocean trail, and Thalassa sunset dining.
                        </p>
                        <div class="guide-progress-bar-wrap">
                            <div class="guide-progress-fill" id="guideProgressFill" style="width: 0%;"></div>
                        </div>
                    </div>

                    <!-- Interactive Route Map Visualizer (With Airport, Cab & Hotel Pins) -->
                    <div class="section-title-wrap">
                        <div>
                            <h3 class="section-title"><span class="sparkle">✦</span> Route Map & Transit Waypoints</h3>
                            <p class="section-subtitle">Live GPS airport, cab corridor & hotel pins</p>
                        </div>
                        <button class="gold-badge" style="cursor:pointer;" onclick="openCurrentDayGoogleMap()">
                            <i class="fa-solid fa-map-location-dot"></i> Maps
                        </button>
                    </div>
                    <div class="route-map-box">
                        <svg class="map-svg-canvas" id="routeMapSvg" viewBox="0 0 400 200"></svg>
                        <div class="map-info-badge" id="mapInfoBadge">
                            <i class="fa-solid fa-route"></i> Route Mapped: Airport ➔ Cab ➔ Villa ➔ Waypoints
                        </div>
                    </div>

                    <!-- Creator Secret Tip Banner -->
                    <div class="insider-tip-box" id="guideCreatorSecretTip" style="font-size:12px; padding:10px 14px; margin-bottom:18px;">
                        <strong>✦ Creator Secret Tip:</strong> Park at Chapora jetty instead of the main hill. Saves 20 mins hike and zero parking scams.
                    </div>

                    <!-- Detailed Schedule Stops Timeline -->
                    <div class="section-title-wrap">
                        <div>
                            <h3 class="section-title"><span class="sparkle">✦</span> Detailed Hourly Itinerary</h3>
                            <p class="section-subtitle">Transit buffers, scenic waypoints & audio stories</p>
                        </div>
                    </div>
                    <div class="stops-timeline" id="guideStopsContainer"></div>

                    <!-- Today's Food Spots -->
                    <div class="section-title-wrap" style="margin-top:20px;">
                        <div>
                            <h3 class="section-title"><span class="sparkle">✦</span> Curated Food Spots</h3>
                            <p class="section-subtitle">Reviewed by @beyondbengalurufoods</p>
                        </div>
                    </div>
                    <div id="guideFoodSpotsContainer"></div>

                </section>

                <!-- ================= TAB 3: CREATOR HUB ================= -->
                <section class="screen-view" id="screen-hub">
                    <div class="section-title-wrap">
                        <div>
                            <span class="gold-badge" style="margin-bottom:6px;">✦ REAL PROOF · ZERO CGI</span>
                            <h2 class="section-title">Creator Video Proofs</h2>
                            <p class="section-subtitle">Watch the actual routes before you book</p>
                        </div>
                    </div>
                    <div id="videoProofsContainer"></div>

                    <div class="section-title-wrap" style="margin-top:24px;">
                        <div>
                            <h3 class="section-title"><span class="sparkle">✦</span> Instagram Proof Wall</h3>
                            <p class="section-subtitle">Live reels and street food reviews</p>
                        </div>
                    </div>
                    <div class="scroll-chips-row">
                        <button class="filter-chip active" onclick="filterReelsChannel('ALL', this)">All Channels</button>
                        <button class="filter-chip" onclick="filterReelsChannel('TRAVEL', this)">📸 @cometriipwme (Travel)</button>
                        <button class="filter-chip" onclick="filterReelsChannel('FOOD', this)">🍜 @beyondbengalurufoods (Food)</button>
                    </div>
                    <div class="reels-grid" id="reelsGridContainer"></div>

                    <div class="section-title-wrap" style="margin-top:24px;">
                        <div>
                            <h3 class="section-title"><span class="sparkle">✦</span> Verified Traveler Reviews</h3>
                            <p class="section-subtitle">Real feedback from travelers who experienced the routes</p>
                        </div>
                    </div>
                    <div id="reviewsContainer"></div>
                </section>

                <!-- ================= TAB 4: TRIP PLANNER (WITH FROM: BLR/DEL/BOM) ================= -->
                <section class="screen-view" id="screen-planner">
                    <div class="section-title-wrap">
                        <div>
                            <span class="gold-badge" style="margin-bottom:6px;">✦ CUSTOM CREATOR ITINERARY</span>
                            <h2 class="section-title">Trip Planner & Flight Builder</h2>
                            <p class="section-subtitle">Choose departure city & get a custom airport itinerary on WhatsApp</p>
                        </div>
                    </div>

                    <!-- Step 1: Departure Airport (From) -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">1</span>
                            <h3 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">Select Departure City (From)</h3>
                        </div>
                        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="plannerFromCity" value="Bengaluru (BLR)" checked onchange="setGlobalOriginCity('BLR')"> BLR · Bengaluru
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="plannerFromCity" value="Delhi (DEL)" onchange="setGlobalOriginCity('DEL')"> DEL · Delhi
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="plannerFromCity" value="Mumbai (BOM)" onchange="setGlobalOriginCity('BOM')"> BOM · Mumbai
                            </label>
                        </div>
                    </div>

                    <!-- Step 2: Destination -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">2</span>
                            <h3 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">Choose Destination (To)</h3>
                        </div>
                        <select class="match-input-select" id="planDestSelect">
                            <option value="Goa (GOX - Mopa & South Goa)">Goa (GOX - Mopa & South Goa)</option>
                            <option value="Thailand (BKK - Bangkok & Krabi)">Thailand (BKK - Bangkok & Krabi)</option>
                            <option value="Himachal Pradesh (KUU - Kasol & Parvati)">Himachal Pradesh (KUU - Kasol & Parvati)</option>
                            <option value="Gokarna Coast (HBX/GOI Gateway)">Gokarna Coast (HBX/GOI Gateway)</option>
                            <option value="Pondicherry (MAA/PNY - French Quarter)">Pondicherry (MAA/PNY - French Quarter)</option>
                            <option value="Malaysia (KLIA - KL & Penang)">Malaysia (KLIA - KL & Penang)</option>
                            <option value="Krabi Islands (KBV)">Krabi Islands (KBV)</option>
                        </select>
                    </div>

                    <!-- Step 3: Vibe -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">3</span>
                            <h3 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">Select Your Vibe</h3>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="planVibe" value="🎉 Party & Nightlife" checked> 🎉 Party
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="planVibe" value="🎒 Backpacking & Adventure"> 🎒 Backpacking
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="planVibe" value="🏔️ Chill & Nature"> 🏔️ Chill
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:6px; cursor:pointer;">
                                <input type="radio" name="planVibe" value="✨ Luxury & Leisure"> ✨ Luxury
                            </label>
                        </div>
                    </div>

                    <!-- Step 4: Squad & Dates -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">4</span>
                            <h3 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">Squad & Approximate Dates</h3>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                            <div>
                                <label class="match-field-label">Squad Size</label>
                                <select class="match-input-select" id="planSquadSelect">
                                    <option value="2 People (Couples/Duo)">2 People (Couples/Duo)</option>
                                    <option value="Solo Traveler">Solo Traveler</option>
                                    <option value="Squad of 3-5">Squad of 3-5</option>
                                    <option value="Group 6+">Group 6+</option>
                                </select>
                            </div>
                            <div>
                                <label class="match-field-label">Tentative Month/Date</label>
                                <input type="text" class="match-input-text" id="planDateInput" placeholder="e.g. Next Friday / Oct 15">
                            </div>
                        </div>
                    </div>

                    <!-- Step 5: Budget & Special Requests -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">5</span>
                            <h3 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">Estimated Budget & Preferences</h3>
                        </div>
                        <div style="margin-bottom:12px;">
                            <label class="match-field-label">Approx Budget Per Person</label>
                            <input type="text" class="match-input-text" id="planBudgetInput" placeholder="e.g. ₹10,000 - ₹15,000">
                        </div>
                        <div>
                            <label class="match-field-label">Special Requests / Cab Preferences</label>
                            <textarea class="match-input-text" id="planNotesInput" rows="3" placeholder="e.g. Airport cab pickup required, scooter rental, pure veg food, pet friendly..."></textarea>
                        </div>
                    </div>

                    <!-- Generate Inquiry Button -->
                    <div style="margin-top:20px; display:flex; flex-direction:column; gap:10px;">
                        <button class="gold-btn" style="padding:16px;" onclick="sendCustomPlannerWhatsApp()">
                            <i class="fa-brands fa-whatsapp" style="font-size:18px;"></i> Send Inquiry to WhatsApp (+91 97423 11023)
                        </button>
                        <button class="glass-btn" onclick="sendCustomPlannerEmail()">
                            <i class="fa-solid fa-envelope"></i> Send via Email
                        </button>
                    </div>

                </section>

                <!-- ================= TAB 5: SAVED TRIPS & PACKING ================= -->
                <section class="screen-view" id="screen-saved">
                    <div class="section-title-wrap">
                        <div>
                            <span class="gold-badge" style="margin-bottom:6px;">✦ YOUR SAVED HUB</span>
                            <h2 class="section-title">Saved Trips & Packing</h2>
                            <p class="section-subtitle">Wishlisted creator routes and live trip packing checklist</p>
                        </div>
                    </div>

                    <div class="section-title-wrap">
                        <div>
                            <h3 class="section-title"><span class="sparkle">✦</span> Wishlist (<span id="wishlistCount">0</span>)</h3>
                        </div>
                    </div>
                    <div id="wishlistContainer" style="margin-bottom:24px;"></div>

                    <div class="glass-panel">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <div>
                                <h3 class="section-title"><span class="sparkle">✦</span> Smart Packing Checklist</h3>
                                <p class="section-subtitle" id="packingProgressText">0 / 6 items packed (0%)</p>
                            </div>
                            <button class="gold-badge" style="cursor:pointer;" onclick="promptAddPackingItem()">
                                <i class="fa-solid fa-plus"></i> Add Item
                            </button>
                        </div>
                        <div class="scroll-chips-row" style="margin-bottom:12px;">
                            <button class="filter-chip active" onclick="filterPackingCategory('ALL', this)">All</button>
                            <button class="filter-chip" onclick="filterPackingCategory('Essentials', this)">Essentials</button>
                            <button class="filter-chip" onclick="filterPackingCategory('Tech', this)">Tech</button>
                            <button class="filter-chip" onclick="filterPackingCategory('Apparel', this)">Apparel</button>
                            <button class="filter-chip" onclick="filterPackingCategory('Care', this)">Care</button>
                            <button class="filter-chip" onclick="filterPackingCategory('Personal', this)">Personal</button>
                        </div>
                        <div id="packingListContainer"></div>
                    </div>
                </section>

            </main>

            <!-- Bottom Navbar -->
            <nav class="app-bottom-navbar">
                <button class="nav-item-btn active" id="navBtn-explore" onclick="switchTab('explore')">
                    <i class="fa-solid fa-compass"></i>
                    <span>Explore</span>
                </button>
                <button class="nav-item-btn" id="navBtn-guide" onclick="switchTab('guide')">
                    <i class="fa-solid fa-headphones"></i>
                    <span>Guide</span>
                </button>
                <button class="nav-item-btn" id="navBtn-hub" onclick="switchTab('hub')">
                    <i class="fa-solid fa-play"></i>
                    <span>Proof</span>
                </button>
                <button class="nav-item-btn" id="navBtn-planner" onclick="switchTab('planner')">
                    <i class="fa-solid fa-calendar-days"></i>
                    <span>Custom</span>
                </button>
                <button class="nav-item-btn" id="navBtn-saved" onclick="switchTab('saved')">
                    <i class="fa-solid fa-bookmark"></i>
                    <span>Saved</span>
                </button>
            </nav>

            <!-- Sticky Audio Player Bar -->
            <div class="live-audio-player-bar" id="audioPlayerBar">
                <div class="audio-player-left" onclick="openAudioStoryDetailModal()">
                    <div class="audio-wave-anim" id="audioWaveAnim">
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                    </div>
                    <div class="audio-title-wrap">
                        <div class="audio-story-title" id="barStoryTitle">Chapora Fort Sunrise</div>
                        <div class="audio-narrator" id="barStoryNarrator">✦ ComeTripWithMe Audio Guide</div>
                    </div>
                </div>
                <div class="audio-player-controls">
                    <button class="audio-play-btn" id="barPlayPauseBtn" onclick="toggleAudioNarration()">
                        <i class="fa-solid fa-play" id="barPlayIcon"></i>
                    </button>
                    <button class="icon-circle-btn" style="width:32px; height:32px;" onclick="stopAudioNarration()" title="Close Player">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </div>

        </div>
    </div>
</div>

<!-- ================= MODAL: DIGITAL BOARDING PASS & LIVE COMPANION ================= -->
<div class="modal-backdrop" id="boardingPassModal">
    <div class="modal-dialog">
        <div class="modal-header">
            <div>
                <span class="gold-badge" style="margin-bottom:4px;">✦ OFFICIAL AIRPORT BOARDING PASS</span>
                <h3 class="modal-title" id="passModalTripName">Goa Long Weekend</h3>
            </div>
            <button class="modal-close-btn" onclick="closeModal('boardingPassModal')">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        <div class="modal-body" id="passModalBody"></div>
        <div class="modal-footer">
            <button class="glass-btn" onclick="closeModal('boardingPassModal')">Close</button>
            <button class="gold-btn" id="passLaunchGuideBtn" onclick="closeModal('boardingPassModal'); switchTab('guide');">
                <i class="fa-solid fa-location-dot"></i> Open Live Guide & Map
            </button>
        </div>
    </div>
</div>

<!-- ================= MODAL: TRIP DETAIL ================= -->
<div class="modal-backdrop" id="tripDetailModal">
    <div class="modal-dialog">
        <div class="modal-header">
            <h3 class="modal-title" id="modalTripName">Goa Long Weekend</h3>
            <button class="modal-close-btn" onclick="closeModal('tripDetailModal')">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        <div class="modal-body" id="modalTripBody"></div>
        <div class="modal-footer">
            <button class="glass-btn" onclick="closeModal('tripDetailModal')">Close</button>
            <button class="gold-btn" id="modalStartGuideBtn">
                <i class="fa-solid fa-ticket"></i> Book & Activate Pass
            </button>
        </div>
    </div>
</div>

<!-- ================= MODAL: AUDIO STORY SCRIPT ================= -->
<div class="modal-backdrop" id="audioScriptModal">
    <div class="modal-dialog">
        <div class="modal-header">
            <div>
                <span class="gold-badge" style="margin-bottom:4px;">✦ LIVE AUDIO GUIDE</span>
                <h3 class="modal-title" id="scriptModalTitle">Chapora Fort: The Secret Sunrise View</h3>
            </div>
            <button class="modal-close-btn" onclick="closeModal('audioScriptModal')">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        <div class="modal-body">
            <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-lg); padding:16px; margin-bottom:16px;">
                <p style="font-size:13px; color:var(--text-secondary); line-height:1.6; font-style:italic;" id="scriptModalText">
                    "Look past the main brick arches toward the northern cliff edge..."
                </p>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <label class="match-field-label" style="margin:0;">Speed:</label>
                    <button class="filter-chip active" id="speedBtn-1" onclick="setSpeechRate(1.0, this)">1.0x</button>
                    <button class="filter-chip" id="speedBtn-125" onclick="setSpeechRate(1.25, this)">1.25x</button>
                </div>
                <button class="gold-btn" onclick="toggleAudioNarration()">
                    <i class="fa-solid fa-play" id="modalPlayBtnIcon"></i> Play Narration
                </button>
            </div>
        </div>
    </div>
</div>

<!-- ================= MODAL: VIDEO PROOF PLAYER ================= -->
<div class="modal-backdrop" id="videoProofModal">
    <div class="modal-dialog" style="max-width:720px;">
        <div class="modal-header">
            <h3 class="modal-title" id="videoModalTitle">Video Proof</h3>
            <button class="modal-close-btn" onclick="closeModal('videoProofModal')">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>
        <div class="modal-body" style="padding:0;">
            <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
                <iframe id="videoModalIframe" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            <div style="padding:16px;" id="videoModalDetails"></div>
        </div>
    </div>
</div>

<!-- ================= MASTER CONTROLLER / CMS DRAWER ================= -->
<div class="cms-drawer-panel" id="cmsDrawer">
    <div class="cms-header">
        <div>
            <span style="font-size:10px; color:#FF8F80; font-weight:800; text-transform:uppercase;">Master App Control Center</span>
            <h3 style="font-family:var(--font-heading); font-size:16px; font-weight:800; color:#fff;">⚙️ Live App CMS & Controller</h3>
        </div>
        <button class="modal-close-btn" onclick="toggleCmsDrawer()">
            <i class="fa-solid fa-xmark"></i>
        </button>
    </div>
    
    <div class="cms-body">
        <div class="cms-tabs-row">
            <button class="cms-tab-btn active" onclick="switchCmsTab('brand', this)">Branding & Contacts</button>
            <button class="cms-tab-btn" onclick="switchCmsTab('transit', this)">Airport Transit Hubs</button>
            <button class="cms-tab-btn" onclick="switchCmsTab('trips', this)">Trips & Days</button>
            <button class="cms-tab-btn" onclick="switchCmsTab('audio', this)">Audio Stories</button>
            <button class="cms-tab-btn" onclick="switchCmsTab('data', this)">Data Export / Reset</button>
        </div>

        <!-- CMS Tab 1: Brand & Contact Info -->
        <div id="cms-section-brand">
            <div class="match-field-group">
                <label class="match-field-label">Brand Title</label>
                <input type="text" class="match-input-text" id="cmsBrandTitle" value="COMETRIPWITHME">
            </div>
            <div class="match-field-group">
                <label class="match-field-label">Brand Subtitle</label>
                <input type="text" class="match-input-text" id="cmsBrandSubtitle" value="India's 1st Creator Tour Operator">
            </div>
            <div class="match-field-group">
                <label class="match-field-label">WhatsApp Contact Number (with country code)</label>
                <input type="text" class="match-input-text" id="cmsWhatsAppNum" value="919742311023">
            </div>
            <div class="match-field-group">
                <label class="match-field-label">Official Phone Number</label>
                <input type="text" class="match-input-text" id="cmsPhoneNum" value="+91 97423 11023">
            </div>
            <div class="match-field-group">
                <label class="match-field-label">Official Email</label>
                <input type="text" class="match-input-text" id="cmsEmail" value="bengalurufoodss@gmail.com">
            </div>
            <div class="match-field-group">
                <label class="match-field-label">Instagram Handles</label>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <input type="text" class="match-input-text" id="cmsHandleTravel" value="@cometriipwme">
                    <input type="text" class="match-input-text" id="cmsHandleFood" value="@beyondbengalurufoods">
                </div>
            </div>
            <div style="margin-top:16px;">
                <button class="gold-btn" style="width:100%;" onclick="saveCmsBranding()">
                    <i class="fa-solid fa-floppy-disk"></i> Save & Apply Branding
                </button>
            </div>
        </div>

        <!-- CMS Tab 2: Airport Transit Manager -->
        <div id="cms-section-transit" style="display:none;">
            <p style="font-size:12px; color:var(--text-secondary); margin-bottom:12px;">Live edit destination airports (GOX, BKK, KUU, KBV, MAA, KLIA) and multi-city flight routes (BLR, DEL, BOM).</p>
            <div id="cmsTransitEditorContainer"></div>
        </div>

        <!-- CMS Tab 3: Trips & Days Manager -->
        <div id="cms-section-trips" style="display:none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:12px; color:var(--text-secondary);">Manage All Curated Trips</span>
                <button class="gold-badge" style="cursor:pointer;" onclick="promptAddNewTrip()">
                    <i class="fa-solid fa-plus"></i> Add New Trip
                </button>
            </div>
            <div id="cmsTripsListContainer"></div>
        </div>

        <!-- CMS Tab 4: Audio Stories Manager -->
        <div id="cms-section-audio" style="display:none;">
            <p style="font-size:12px; color:var(--text-secondary); margin-bottom:14px;">Live edit speech synthesis narration scripts across all trips.</p>
            <div id="cmsAudioStoriesList"></div>
        </div>

        <!-- CMS Tab 5: Data Management -->
        <div id="cms-section-data" style="display:none;">
            <div class="glass-panel" style="padding:14px; margin-bottom:14px;">
                <h4 style="font-size:14px; font-weight:800; color:#fff; margin-bottom:6px;">Export Full App JSON</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Download the entire current database as a portable JSON file.</p>
                <button class="gold-btn" style="padding:8px 16px; font-size:12px;" onclick="exportAppDataJson()">
                    <i class="fa-solid fa-download"></i> Export JSON
                </button>
            </div>

            <div class="glass-panel" style="padding:14px; margin-bottom:14px;">
                <h4 style="font-size:14px; font-weight:800; color:#fff; margin-bottom:6px;">Import JSON Database</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Upload a modified JSON backup to update all itineraries instantly.</p>
                <input type="file" id="cmsJsonFileInput" accept=".json" style="display:none;" onchange="importAppDataJson(event)">
                <button class="glass-btn" style="padding:8px 16px; font-size:12px;" onclick="document.getElementById('cmsJsonFileInput').click()">
                    <i class="fa-solid fa-upload"></i> Import JSON
                </button>
            </div>

            <div class="glass-panel" style="padding:14px; border-color:rgba(220, 80, 60, 0.4);">
                <h4 style="font-size:14px; font-weight:800; color:#FFA090; margin-bottom:6px;">Reset to Factory Curated Data</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Revert all changes back to original ComeTripWithMe default data.</p>
                <button class="glass-btn" style="border-color:rgba(220, 80, 60, 0.6); color:#FFA090;" onclick="resetToFactoryCuratedData()">
                    <i class="fa-solid fa-rotate-left"></i> Factory Reset Database
                </button>
            </div>
        </div>

    </div>
</div>

<!-- Toast Container -->
<div class="toast-container" id="toastContainer"></div>

<!-- Complete Embedded Database & Reactive JS Controller -->
<script>
/**
 * COMETRIPWITHME - MASTER DATA & REACTIVE LOGIC ENGINE WITH AIRPORT HUBS & MULTI-CITY DEPARTURES (BLR / DEL / BOM)
 */

const FACTORY_DATA = {
    branding: {
        title: "COMETRIPWITHME",
        subtitle: "India's 1st Creator Tour Operator",
        whatsapp: "919742311023",
        phone: "+91 97423 11023",
        email: "bengalurufoodss@gmail.com",
        instagramTravel: "@cometriipwme",
        instagramFood: "@beyondbengalurufoods",
        youtube: "Cometripwithme"
    },
    userBooking: {
        passengerName: "Karthik Dalabanjan",
        bookingId: "CTWM-GOA-8842",
        bookedTripId: "goa",
        departureOrigin: "BLR", // BLR, DEL, BOM
        squadSize: "2 of us",
        travelDate: "Upcoming Friday",
        status: "CONFIRMED & TICKETED"
    },
    origins: {
        "BLR": { code: "BLR", name: "Bengaluru", airport: "Kempegowda Intl (BLR)", terminal: "T2", color: "#38BDF8" },
        "DEL": { code: "DEL", name: "Delhi", airport: "Indira Gandhi Intl (DEL)", terminal: "T3", color: "#E8C97A" },
        "BOM": { code: "BOM", name: "Mumbai", airport: "Chhatrapati Shivaji Maharaj (BOM)", terminal: "T2", color: "#86EFAC" }
    },
    spotlights: [
        {
            id: "hampi",
            title: "Hampi & Badami Ruins",
            subtitle: "Boulders, Vijayanagara empire & Tungabhadra sunsets",
            region: "VDY / HBX Gateway · UNESCO World Heritage",
            airportTag: "VDY · Jindal Vijayanagar",
            imageUrl: "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?w=800&q=80"
        },
        {
            id: "thailand_spot",
            title: "Thailand & Islands",
            subtitle: "Bangkok street food woks & Krabi emerald lagoons",
            region: "BKK / KBV Gateways · Southeast Asia",
            airportTag: "BKK · Suvarnabhumi",
            imageUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80"
        },
        {
            id: "himachal_spot",
            title: "Parvati Valley & Kasol",
            subtitle: "Pine forests, hot spring treks & river cafes",
            region: "KUU Gateway · Himalayan Foothills",
            airportTag: "KUU · Kullu-Manali",
            imageUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80"
        },
        {
            id: "gokarna_spot",
            title: "Gokarna Coast",
            subtitle: "5-beach cliff trail, secret Half Moon camps",
            region: "HBX / GOI Gateway · Karnataka Coast",
            airportTag: "HBX · Hubballi",
            imageUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80"
        }
    ],
    trips: [
        {
            id: "goa",
            name: "Goa Long Weekend",
            headline: "Beach days, cliffside sundowners, zero tourist traps.",
            description: "Forget crowded commercial packages. We hit the real North Goa secret spots, cliff viewpoints, legendary bakeries, and wind down with tranquil South Goa kayaking.",
            vibe: "PARTY",
            duration: "4D · 3N",
            price: "₹8,999",
            budgetValue: 8999,
            imageUrl: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80",
            heroTags: ["GOX Mopa Airport", "Cliff Views", "Kayaking", "Secret Bakeries"],
            totalEstimateDetails: "Includes 3 nights boutique villa stay, airport AC cab transfers, scooty fuel allowance & food pass.",
            creatorNote: "We scouted every single stop in December 2024 to make sure the vibe is completely untarnished.",
            
            // Primary & Alternate Airport Restructuring
            airportInfo: {
                primaryCode: "GOX",
                primaryName: "Goa Manohar International Airport (Mopa, North Goa)",
                alternateCode: "GOI",
                alternateName: "Dabolim International Airport (South Goa)",
                arrivalTerminal: "Terminal 1",
                baggageCarousel: "Belt 3"
            },

            // Multi-Origin Transit Matrix for BLR, DEL, BOM
            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "Flight 6E-204 (Airbus A321)",
                    terminal: "Kempegowda Intl (BLR) · Terminal 2",
                    gate: "Gate 14B",
                    boardingTime: "05:45 AM",
                    departureTime: "06:30 AM",
                    arrivalTime: "07:45 AM",
                    duration: "1h 15m (Non-Stop)",
                    pnr: "CTWM-BLR-GOX"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "Flight 6E-6125 / AI-847",
                    terminal: "Indira Gandhi Intl (DEL) · Terminal 3",
                    gate: "Gate 32A",
                    boardingTime: "06:30 AM",
                    departureTime: "07:15 AM",
                    arrivalTime: "09:50 AM",
                    duration: "2h 35m (Non-Stop)",
                    pnr: "CTWM-DEL-GOX"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "Flight 6E-5381 / QP-1382",
                    terminal: "Chhatrapati Shivaji Maharaj (BOM) · Terminal 2",
                    gate: "Gate 48B",
                    boardingTime: "06:00 AM",
                    departureTime: "06:45 AM",
                    arrivalTime: "07:55 AM",
                    duration: "1h 10m (Non-Stop)",
                    pnr: "CTWM-BOM-GOX"
                }
            },

            cabTransfer: {
                pickupLocation: "Airport Arrival Gate 3 · Ride-Share Zone B (Bay 4)",
                vehicle: "Innova Crysta Luxury (GA-03-Z-8842)",
                driverName: "Ramesh Naik (Verified Partner)",
                driverPhone: "+919742311023",
                durationToHotel: "45 mins scenic drive (34 km)"
            },

            hotelStay: {
                name: "Thalassa Luxury Cliffside Villa & Resort",
                address: "Plot 14, Small Vagator Cliff Trail, North Goa 403509",
                mapLink: "https://maps.google.com/?q=Vagator+Goa",
                checkInTime: "10:30 AM (Early check-in confirmed)",
                checkOutTime: "12:00 PM",
                roomType: "Oceanview Bohemian Suite with Private Balcony",
                wifiSsid: "Thalassa_Guest_5G",
                wifiPass: "sunsetcurator2025",
                hostName: "Dimitri (Host Concierge)",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "North Goa Secret Cliffs & Bakeries",
                    summary: "Sunrise scooter crawl, Chapora cliff panoramas, hidden Anjuna ocean trail, and Thalassa sunset dining.",
                    creatorSecretTip: "Park at Chapora jetty instead of the main hill. Saves 20 mins hike and zero parking scams.",
                    stops: [
                        {
                            id: "goa_d1_s1",
                            name: "Chapora Fort Sunrise Point",
                            timing: "06:30 AM",
                            interStopTransit: "🚖 45 mins airport cab transfer to Vagator + 10 mins scooty crawl",
                            category: "Cliff Viewpoint",
                            description: "Ancient red-laterite fort ramparts overlooking the vast Vagator and Morjim ocean mouth.",
                            insiderTip: "Walk past the main entrance to the secluded northern corner for 0-tourist photographs.",
                            photoUrl: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80",
                            lat: 15.6067,
                            lng: 73.7371,
                            audioStory: {
                                title: "Chapora Fort: The Secret Sunrise View",
                                durationSeconds: 85,
                                scriptText: "Look past the main brick arches toward the northern cliff edge. While everyone flocks here at sunset for the Bollywood Dil Chahta Hai pose, the early morning light reveals the calmest waters and cool Arabian breeze without a single crowd."
                            }
                        },
                        {
                            id: "goa_d1_s2",
                            name: "Anjuna Rocky Beach Trail",
                            timing: "10:00 AM",
                            interStopTransit: "🛵 12 mins scooty ride (4.6 km) via Anjuna-Chapora Road",
                            category: "Scenic Coast",
                            description: "Red volcanic rock formations with natural ocean tidepools and breezy coconut palms.",
                            insiderTip: "Wear grippy footwear; the black volcanic rock gets slippery near the water line.",
                            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                            lat: 15.5833,
                            lng: 73.7431
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Thalassa Greek Taverna",
                            specialty: "Greek cuisine & sunset cocktail",
                            mustTryDish: "Souvlaki wraps & Baklava",
                            approxCostForTwo: "₹1,800 for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80"
                        }
                    ]
                },
                {
                    dayNumber: 2,
                    title: "South Goa Tranquil Switch & Kayaking",
                    summary: "Drive down through Portuguese village lanes to Palolem's crescent bay and secret butterfly cove.",
                    creatorSecretTip: "Ask fishermen at Palolem south end for a shared boat ride to Butterfly Beach — ₹400 per person.",
                    stops: [
                        {
                            id: "goa_d2_s1",
                            name: "Palolem Crescent Beach",
                            timing: "11:00 AM",
                            interStopTransit: "🚗 1 hr 45 mins private AC transfer down to South Goa (68 km)",
                            category: "Calm Beach",
                            description: "Gentle bay framed by lush coconut groves, colorful wooden shacks, and dolphins.",
                            insiderTip: "Rent a single kayak for ₹300/hr and paddle around Canacona Island.",
                            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                            lat: 15.0100,
                            lng: 74.0231,
                            audioStory: {
                                title: "Palolem: The Secret Dolphin Sanctuary",
                                durationSeconds: 95,
                                scriptText: "Notice how calm the water is here compared to North Goa? Palolem is a natural amphitheater of granite headlands. If you kayak out 300 meters early morning, Indo-Pacific humpback dolphins frequently surface right next to your boat."
                            }
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Dropadi Beach Restaurant",
                            specialty: "Fresh catch of the day on Palolem beach",
                            mustTryDish: "Butter Garlic Squid & Coconut Rice",
                            approxCostForTwo: "₹950 for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&q=80"
                        }
                    ]
                }
            ]
        },
        {
            id: "thailand",
            name: "Thailand & Krabi",
            headline: "Street food at midnight. Emerald islands at sunrise.",
            description: "7 days across electric Bangkok street food alleyways and the dramatic limestone sea cliffs of Krabi. We bypass overpriced tours and show you the exact local ferries and food carts.",
            vibe: "BACKPACKING",
            duration: "7D · 6N",
            price: "₹24,999",
            budgetValue: 24999,
            imageUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
            heroTags: ["BKK Suvarnabhumi", "Krabi KBV", "Longtail Boats", "Night Markets"],
            totalEstimateDetails: "Covers 3N Bangkok boutique hotel, 3N Krabi beachfront resort, 4 Islands longtail tour & street food crawl.",
            creatorNote: "Bangkok street food is best at 11 PM in Chinatown. We mapped the exact 4 stalls that locals eat at.",
            
            airportInfo: {
                primaryCode: "BKK",
                primaryName: "Bangkok Suvarnabhumi International Airport",
                alternateCode: "DMK",
                alternateName: "Don Mueang International Airport",
                arrivalTerminal: "Level 2 International Arrivals",
                baggageCarousel: "Belt 14"
            },

            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "Thai Airways TG-326 (Boeing 777)",
                    terminal: "Kempegowda (BLR) · T2 International",
                    gate: "Gate 22A",
                    boardingTime: "11:45 PM",
                    departureTime: "00:45 AM",
                    arrivalTime: "06:15 AM",
                    duration: "4h 00m (Non-Stop)",
                    pnr: "CTWM-BLR-BKK"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "Air India AI-332 (Boeing 787 Dreamliner)",
                    terminal: "Indira Gandhi (DEL) · T3 International",
                    gate: "Gate 18B",
                    boardingTime: "01:15 PM",
                    departureTime: "02:05 PM",
                    arrivalTime: "07:55 PM",
                    duration: "4h 20m (Non-Stop)",
                    pnr: "CTWM-DEL-BKK"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "IndiGo 6E-1053 / Thai Airways TG-318",
                    terminal: "CSMIA (BOM) · T2 International",
                    gate: "Gate 64",
                    boardingTime: "03:45 AM",
                    departureTime: "04:30 AM",
                    arrivalTime: "10:30 AM",
                    duration: "4h 30m (Non-Stop)",
                    pnr: "CTWM-BOM-BKK"
                }
            },

            cabTransfer: {
                pickupLocation: "BKK Level 1 Public Van/Limo Gate 3",
                vehicle: "Toyota Commuter VIP Van (1-Kor-4492)",
                driverName: "Somchai Kittisuk",
                driverPhone: "+919742311023",
                durationToHotel: "35 mins via Sirat Expressway (28 km)"
            },

            hotelStay: {
                name: "ASAI Bangkok Chinatown Hotel",
                address: "531 Charoen Krung Rd, Pom Prap, Bangkok 10100",
                mapLink: "https://maps.google.com/?q=ASAI+Bangkok+Chinatown",
                checkInTime: "12:00 PM (Luggage drop at 07:45 AM)",
                checkOutTime: "11:00 AM",
                roomType: "Comfy King Room with Courtyard View",
                wifiSsid: "ASAI_Guest_HighSpeed",
                wifiPass: "chinatownwok2025",
                hostName: "Ploy (Guest Lead)",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "Bangkok Chinatown & Neon Food Crawl",
                    summary: "Arrive at Suvarnabhumi, take Airport Rail Link, check into Chinatown boutique stay, and explore 40-year-old roaring woks.",
                    creatorSecretTip: "Skip tuk-tuks on main Yaowarat road; walk down the small soi lanes for half-priced woks.",
                    stops: [
                        {
                            id: "th_d1_s1",
                            name: "Yaowarat Chinatown Main Strip",
                            timing: "07:00 PM",
                            interStopTransit: "🚶 4 mins walk from ASAI Hotel courtyard",
                            category: "Food Street",
                            description: "Dazzling neon lights, sizzling charcoal woks, and world-famous street food stalls.",
                            insiderTip: "Look for stalls with long queues of local Thai families, not just tourists.",
                            photoUrl: "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
                            lat: 13.7408,
                            lng: 100.5108,
                            audioStory: {
                                title: "Chinatown Yaowarat: 40 Years of Sizzling Woks",
                                durationSeconds: 110,
                                scriptText: "Listen to the roar of that high-pressure wok burner. This alley has been serving crispy oyster omelets and pepper broth noodles since 1978. The secret is the pork bone stock simmered continuously for over 18 hours."
                            }
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Nai Ek Roll Noodle",
                            specialty: "Crispy pork belly in peppery broth",
                            mustTryDish: "Guay Jub Crispy Pork Noodle",
                            approxCostForTwo: "160 THB for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&q=80"
                        }
                    ]
                }
            ]
        },
        {
            id: "himachal",
            name: "Himachal Pradesh",
            headline: "The mountains will fix whatever is broken in you.",
            description: "Riverside Kasol cafés, Kheerganga hot springs trek, Solang snow peaks, and serene pine forest walks. Authentic homestays and zero commercial tourist jams.",
            vibe: "CHILL",
            duration: "5D · 4N",
            price: "₹11,999",
            budgetValue: 11999,
            imageUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
            heroTags: ["KUU Bhuntar Airport", "Parvati River", "Old Manali", "Hot Springs"],
            totalEstimateDetails: "Includes 4 nights wooden cottage stay, Kheerganga guide, daily hearty mountain breakfasts.",
            creatorNote: "The riverside homestay in Tosh has the clearest view of the snowline in the entire valley.",
            
            airportInfo: {
                primaryCode: "KUU",
                primaryName: "Kullu-Manali Airport (Bhuntar, Himachal)",
                alternateCode: "IXC",
                alternateName: "Chandigarh International Airport",
                arrivalTerminal: "Main Terminal",
                baggageCarousel: "Main Gate"
            },

            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "Flight 6E-243 to Chandigarh (IXC) + Luxury AC Cab",
                    terminal: "Kempegowda (BLR) · Terminal 1",
                    gate: "Gate 8",
                    boardingTime: "06:15 AM",
                    departureTime: "07:00 AM",
                    arrivalTime: "09:55 AM (IXC) / 04:30 PM (Kasol)",
                    duration: "2h 55m flight + scenic mountain transfer",
                    pnr: "CTWM-BLR-KUU"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "Alliance Air 9I-805 (Direct to Bhuntar KUU) / Volvo 9600",
                    terminal: "Indira Gandhi (DEL) · Terminal 2",
                    gate: "Gate 12",
                    boardingTime: "06:15 AM",
                    departureTime: "06:55 AM",
                    arrivalTime: "08:15 AM (Bhuntar Airport)",
                    duration: "1h 20m (Direct Flight)",
                    pnr: "CTWM-DEL-KUU"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "Flight AI-651 to Chandigarh (IXC) + Mountain Cab",
                    terminal: "CSMIA (BOM) · Terminal 2",
                    gate: "Gate 34",
                    boardingTime: "06:40 AM",
                    departureTime: "07:25 AM",
                    arrivalTime: "09:45 AM (IXC) / 04:30 PM (Kasol)",
                    duration: "2h 20m flight + transfer",
                    pnr: "CTWM-BOM-KUU"
                }
            },

            cabTransfer: {
                pickupLocation: "Chalal Suspension Bridge Car Park",
                vehicle: "Mahindra Scorpio 4x4 (HP-34-A-1102)",
                driverName: "Tenzing Negi",
                driverPhone: "+919742311023",
                durationToHotel: "15 mins mountain trail drive (4.2 km)"
            },

            hotelStay: {
                name: "Parvati Woods Riverside Wooden Cottages",
                address: "Old Chalal Pine Forest Trail, Kasol, Himachal 175105",
                mapLink: "https://maps.google.com/?q=Kasol+Himachal",
                checkInTime: "10:00 AM",
                checkOutTime: "11:00 AM",
                roomType: "Attic Cedar Wood Room with River Stream Balcony",
                wifiSsid: "Parvati_Woods_Fiber",
                wifiPass: "himalayanchill2025",
                hostName: "Sunny Thakur",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "Kasol Riverside & German Bakery Crawl",
                    summary: "Wake up to roaring Parvati river waters, hot honey ginger lemon tea, and fresh apple crumble.",
                    creatorSecretTip: "Cross the suspension bridge over Parvati river to find the quieter pine forest cafes.",
                    stops: [
                        {
                            id: "him_d1_s1",
                            name: "Parvati River Stone Bank",
                            timing: "08:00 AM",
                            interStopTransit: "🚶 5 mins scenic pine walk from cottage",
                            category: "Mountain River",
                            description: "Crystal clear glacial waters crashing against massive riverbed boulders with pine backdrop.",
                            insiderTip: "Sit by the quieter stretch near Chalal bridge for total silence.",
                            photoUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=600&q=80",
                            lat: 32.0100,
                            lng: 77.3150,
                            audioStory: {
                                title: "Parvati Valley: The Himalayan Soundscape",
                                durationSeconds: 90,
                                scriptText: "Breathe in the scent of fresh pine needles and cedar wood. That roar you hear is the Parvati river, fed by the glacial melt of the Pin Parvati pass over 5,000 meters above."
                            }
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Moon Dance Café Kasol",
                            specialty: "German bakery & Israeli shakshuka",
                            mustTryDish: "Fresh Apple Strudel with Vanilla Custard",
                            approxCostForTwo: "₹550 for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80"
                        }
                    ]
                }
            ]
        },
        {
            id: "krabi",
            name: "Krabi Island Escapes",
            headline: "The kind of turquoise water that breaks your camera settings.",
            description: "5 days in paradise. Railay peninsula cliffs, 4 Islands longtail cruise, emerald freshwater lagoons, and sunset beach seafood barbecues.",
            vibe: "LUXURY",
            duration: "5D · 4N",
            price: "₹28,999",
            budgetValue: 28999,
            imageUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
            heroTags: ["KBV Krabi Airport", "Railay Cliffs", "Emerald Pool", "Sunset BBQ"],
            totalEstimateDetails: "Includes 4 nights 5-star beachfront resort, private longtail charter, all national park entry fees.",
            creatorNote: "We booked a private traditional longtail with local captain Somchai — no loudspeaker tour guides.",
            
            airportInfo: {
                primaryCode: "KBV",
                primaryName: "Krabi International Airport",
                alternateCode: "HKT",
                alternateName: "Phuket International Airport",
                arrivalTerminal: "Terminal 1 Arrivals",
                baggageCarousel: "Belt 2"
            },

            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "AirAsia / Thai Airways (BLR ➔ BKK ➔ KBV)",
                    terminal: "Kempegowda (BLR) · T2 International",
                    gate: "Gate 20",
                    boardingTime: "11:30 PM",
                    departureTime: "00:20 AM",
                    arrivalTime: "09:45 AM (KBV)",
                    duration: "6h 25m (1 seamless connection)",
                    pnr: "CTWM-BLR-KBV"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "IndiGo 6E-1051 to Phuket (HKT) + Speedboat to Railay",
                    terminal: "Indira Gandhi (DEL) · T3",
                    gate: "Gate 15A",
                    boardingTime: "05:15 AM",
                    departureTime: "06:00 AM",
                    arrivalTime: "12:15 PM (HKT)",
                    duration: "4h 45m flight + boat transfer",
                    pnr: "CTWM-DEL-KBV"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "IndiGo / Thai Lion Air (BOM ➔ DMK ➔ KBV)",
                    terminal: "CSMIA (BOM) · T2",
                    gate: "Gate 52",
                    boardingTime: "02:40 AM",
                    departureTime: "03:30 AM",
                    arrivalTime: "11:15 AM (KBV)",
                    duration: "6h 15m (1 quick transfer)",
                    pnr: "CTWM-BOM-KBV"
                }
            },

            cabTransfer: {
                pickupLocation: "Airport Exit Gate 2 Meeting Point",
                vehicle: "Toyota Fortuner 4x4 (กข-5512)",
                driverName: "Captain Bao",
                driverPhone: "+919742311023",
                durationToHotel: "30 mins to Ao Nang Pier + 15 mins private longtail boat to Railay"
            },

            hotelStay: {
                name: "Railay Bay Resort & Spa Beachfront Villas",
                address: "145 M.2 Ao Nang, Muang, Railay Beach, Krabi 81000",
                mapLink: "https://maps.google.com/?q=Railay+Bay+Resort",
                checkInTime: "12:30 PM",
                checkOutTime: "11:00 AM",
                roomType: "Beachfront Pool Villa surrounded by limestone cliffs",
                wifiSsid: "RailayBay_Resort_VIP",
                wifiPass: "emeraldlagoon2025",
                hostName: "Karn (Resort Director)",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "Private 4 Islands Longtail Expedition",
                    summary: "Cruise to Koh Poda, Chicken Island sandbar, Tub Island, and Phra Nang sunset cove.",
                    creatorSecretTip: "Check the tide chart; Tub Island sandbar is only visible at low tide.",
                    stops: [
                        {
                            id: "krabi_d1_s1",
                            name: "Koh Poda & Coral Reef",
                            timing: "09:00 AM",
                            interStopTransit: "🚤 15 mins private traditional longtail boat from Railay West beach",
                            category: "Tropical Island",
                            description: "White powder sand beach facing a dramatic vertical limestone rock tower in turquoise sea.",
                            insiderTip: "Swim 20 meters from the beach tree line to see schools of yellow sergeant major fish.",
                            photoUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
                            lat: 7.9710,
                            lng: 98.8140
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Ao Nang Seafood Promenade",
                            specialty: "Catch of the day grilled over coconut husks",
                            mustTryDish: "Steamed Sea Bass in Spicy Lime & Garlic",
                            approxCostForTwo: "700 THB for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1535400255456-984241443b29?w=600&q=80"
                        }
                    ]
                }
            ]
        },
        {
            id: "gokarna",
            name: "Gokarna Coast",
            headline: "Cliff hikes, hidden crescent coves, and acoustic campfire nights.",
            description: "4 days discovering the raw beauty of coastal Karnataka. The 5-beach cliff trek, Half Moon beach camp, secret lagoons, and oceanfront shacks.",
            vibe: "CHILL",
            duration: "4D · 3N",
            price: "₹6,499",
            budgetValue: 6499,
            imageUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
            heroTags: ["HBX Hubballi Airport", "5 Beach Trek", "Campfire", "Beach Shacks"],
            totalEstimateDetails: "Includes 3 nights oceanfront hut stay, cliff trek guide, beach bonfire and boat transfer.",
            creatorNote: "Half Moon beach is only accessible by foot or boat — totally disconnected from road traffic.",
            
            airportInfo: {
                primaryCode: "HBX",
                primaryName: "Hubballi Airport (Karnataka Gateway)",
                alternateCode: "GOI",
                alternateName: "Goa Dabolim Airport (130 km north)",
                arrivalTerminal: "Terminal 1",
                baggageCarousel: "Belt 1"
            },

            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "Star Air S5-112 (Direct to HBX) / Panchaganga SF Train",
                    terminal: "Kempegowda (BLR) · Terminal 1",
                    gate: "Gate 4",
                    boardingTime: "07:15 AM",
                    departureTime: "07:55 AM",
                    arrivalTime: "09:05 AM (HBX)",
                    duration: "1h 10m flight + scenic cab to Gokarna",
                    pnr: "CTWM-BLR-HBX"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "Flight 6E-2412 to Goa Dabolim (GOI) + Coastal Cab",
                    terminal: "Indira Gandhi (DEL) · Terminal 3",
                    gate: "Gate 24",
                    boardingTime: "06:15 AM",
                    departureTime: "07:00 AM",
                    arrivalTime: "09:40 AM (GOI)",
                    duration: "2h 40m flight + 2.5h coastal highway cab",
                    pnr: "CTWM-DEL-HBX"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "IndiGo 6E-5124 to Hubballi (HBX) / Goa (GOI)",
                    terminal: "CSMIA (BOM) · Terminal 2",
                    gate: "Gate 19",
                    boardingTime: "08:00 AM",
                    departureTime: "08:45 AM",
                    arrivalTime: "10:15 AM (HBX)",
                    duration: "1h 30m flight + cab transfer",
                    pnr: "CTWM-BOM-HBX"
                }
            },

            cabTransfer: {
                pickupLocation: "Airport Auto/Cab Stand Bay 1",
                vehicle: "Maruti Ertiga (KA-47-M-2291)",
                driverName: "Manjunath Gowda",
                driverPhone: "+919742311023",
                durationToHotel: "1 hr 45 mins Western Ghats highway drive"
            },

            hotelStay: {
                name: "Namaste Sanjeevini Ocean Hill Cottages",
                address: "Kudle Beach Hilltop Trail, Gokarna, Karnataka 581326",
                mapLink: "https://maps.google.com/?q=Kudle+Beach+Gokarna",
                checkInTime: "09:00 AM (Early check-in)",
                checkOutTime: "11:00 AM",
                roomType: "Eco Stone Hut overlooking Kudle Sunset Bay",
                wifiSsid: "Sanjeevini_Beach_WiFi",
                wifiPass: "omkudle2025",
                hostName: "Shridhar Hegde",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "The 5-Beach Cliff Trek",
                    summary: "Hike from Kudle beach across the red rocky cliffs down to Om Beach, Half Moon, and Paradise.",
                    creatorSecretTip: "Start at 6:45 AM from Kudle to complete the cliff trail before the mid-day coastal sun.",
                    stops: [
                        {
                            id: "gok_d1_s1",
                            name: "Om Beach Cliff Vantage",
                            timing: "08:00 AM",
                            interStopTransit: "🥾 25 mins cliff path hike from Kudle beach",
                            category: "Coastal Cliff",
                            description: "Natural geological formation resembling the sacred OM symbol from the cliff viewpoint.",
                            insiderTip: "Take the dirt path past Namaste Café to access the quiet rock pool.",
                            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
                            lat: 14.5180,
                            lng: 74.3180
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Namaste Café Gokarna",
                            specialty: "Oceanfront shack dining",
                            mustTryDish: "Nutella Banana Pancake & Cold Coffee",
                            approxCostForTwo: "₹450 for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80"
                        }
                    ]
                }
            ]
        },
        {
            id: "pondicherry",
            name: "Pondicherry French Quarter",
            headline: "French heritage lanes, Indian soul, ₹400 filter coffee & croissants.",
            description: "Cycle through the mustard-yellow French Quarter at 6:30 AM before tourists wake up. Experience spiritual Auroville, golden beaches, and authentic French bakeries.",
            vibe: "CHILL",
            duration: "3D · 2N",
            price: "₹5,499",
            budgetValue: 5499,
            imageUrl: "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=80",
            heroTags: ["MAA / PNY Airport", "Auroville", "Artisan Bakeries", "Cycle Crawl"],
            totalEstimateDetails: "Includes 2 nights heritage villa stay, vintage bicycle rental, bakery breakfast pass.",
            creatorNote: "White Town is best explored on a pastel bicycle at sunrise. Zero car honks, just birds and ocean breeze.",
            
            airportInfo: {
                primaryCode: "MAA",
                primaryName: "Chennai International Airport (2.5h scenic ECR drive)",
                alternateCode: "PNY",
                alternateName: "Puducherry Domestic Airport",
                arrivalTerminal: "Terminal 1",
                baggageCarousel: "Belt 4"
            },

            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "IndiGo 6E-7281 / AC Volvo Coach (KSRTC Club Class)",
                    terminal: "Kempegowda (BLR) / Madiwala St. John's",
                    gate: "Gate 6",
                    boardingTime: "06:15 AM",
                    departureTime: "07:00 AM",
                    arrivalTime: "08:15 AM",
                    duration: "1h 15m flight or 6h overnight sleeper",
                    pnr: "CTWM-BLR-MAA"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "Flight AI-440 to Chennai (MAA) + ECR Highway Cab",
                    terminal: "Indira Gandhi (DEL) · T3",
                    gate: "Gate 28B",
                    boardingTime: "06:00 AM",
                    departureTime: "06:45 AM",
                    arrivalTime: "09:35 AM (MAA)",
                    duration: "2h 50m flight + scenic coastal cab",
                    pnr: "CTWM-DEL-MAA"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "Flight 6E-271 to Chennai (MAA) + ECR Highway Cab",
                    terminal: "CSMIA (BOM) · T2",
                    gate: "Gate 41",
                    boardingTime: "06:30 AM",
                    departureTime: "07:15 AM",
                    arrivalTime: "09:10 AM (MAA)",
                    duration: "1h 55m flight + coastal cab",
                    pnr: "CTWM-BOM-MAA"
                }
            },

            cabTransfer: {
                pickupLocation: "MAA Airport Exit Gate 4 (Private Chauffeur Lane)",
                vehicle: "Toyota Innova Crysta (TN-01-AB-4412)",
                driverName: "Senthil Kumar",
                driverPhone: "+919742311023",
                durationToHotel: "2 hr 15 mins scenic East Coast Road (ECR) drive"
            },

            hotelStay: {
                name: "Maison Perumal - CGH Earth French Heritage Villa",
                address: "44, Perumal Koil St, Heritage Town, Puducherry 605001",
                mapLink: "https://maps.google.com/?q=Maison+Perumal+Pondicherry",
                checkInTime: "08:00 AM (Early luggage check-in & coffee)",
                checkOutTime: "11:00 AM",
                roomType: "Colonial Courtyard Heritage Room",
                wifiSsid: "Maison_Perumal_Guest",
                wifiPass: "frenchquarter2025",
                hostName: "Jean-Pierre & Ananya",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "White Town Sunrise Bicycle Crawl",
                    summary: "Glide past bougainvillea draped French colonial villas, Promenade beach walk, and fresh bakery pastries.",
                    creatorSecretTip: "Baker Street sells out of almond croissants by 9:30 AM. Get there right at opening.",
                    stops: [
                        {
                            id: "pon_d1_s1",
                            name: "Promenade Rock Beach & French War Memorial",
                            timing: "06:15 AM",
                            interStopTransit: "🚲 6 mins pastel vintage bicycle ride from Maison Perumal",
                            category: "Ocean Promenade",
                            description: "1.5 km vehicle-free coastal promenade with crashing Bay of Bengal waves.",
                            insiderTip: "Walk down to the southern pier for the clearest sunrise over the ocean.",
                            photoUrl: "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&q=80",
                            lat: 11.9338,
                            lng: 79.8350
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Coromandel Café",
                            specialty: "French fusion in a restored 19th-century villa",
                            mustTryDish: "Pork belly tacos & Salted Caramel tart",
                            approxCostForTwo: "₹1,400 for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80"
                        }
                    ]
                }
            ]
        },
        {
            id: "malaysia",
            name: "Malaysia & Penang",
            headline: "KL skyline to Penang street food legacy in 4 hours.",
            description: "5 days taking you from the gleaming Petronas Towers and Batu Caves to the UNESCO World Heritage street murals and sizzling hawker stalls of George Town.",
            vibe: "BACKPACKING",
            duration: "5D · 4N",
            price: "₹21,999",
            budgetValue: 21999,
            imageUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80",
            heroTags: ["KLIA Airport", "Penang Hawkers", "Batu Caves", "UNESCO Murals"],
            totalEstimateDetails: "Includes 2N KL skyline apartment, 2N Penang heritage hotel, KTM electric train ticket and food trail.",
            creatorNote: "The KTM train from KL Sentral to Butterworth is faster and more comfortable than flying.",
            
            airportInfo: {
                primaryCode: "KLIA",
                primaryName: "Kuala Lumpur International Airport (Terminal 1 & 2)",
                alternateCode: "PEN",
                alternateName: "Penang International Airport (George Town)",
                arrivalTerminal: "Terminal 1 Arrivals",
                baggageCarousel: "Belt 7"
            },

            originRoutes: {
                "BLR": {
                    originCode: "BLR",
                    originName: "Bengaluru",
                    transport: "Malaysia Airlines MH-193 (Boeing 737-800)",
                    terminal: "Kempegowda (BLR) · T2 International",
                    gate: "Gate 19B",
                    boardingTime: "10:30 PM",
                    departureTime: "11:20 PM",
                    arrivalTime: "06:10 AM (KLIA)",
                    duration: "4h 20m (Non-Stop)",
                    pnr: "CTWM-BLR-KLIA"
                },
                "DEL": {
                    originCode: "DEL",
                    originName: "Delhi",
                    transport: "AirAsia X D7-183 / Malaysia Airlines MH-191",
                    terminal: "Indira Gandhi (DEL) · T3",
                    gate: "Gate 16",
                    boardingTime: "11:15 PM",
                    departureTime: "00:10 AM",
                    arrivalTime: "08:00 AM (KLIA)",
                    duration: "5h 20m (Non-Stop)",
                    pnr: "CTWM-DEL-KLIA"
                },
                "BOM": {
                    originCode: "BOM",
                    originName: "Mumbai",
                    transport: "Batik Air OD-216 / Malaysia Airlines MH-187",
                    terminal: "CSMIA (BOM) · T2",
                    gate: "Gate 72",
                    boardingTime: "10:15 PM",
                    departureTime: "11:05 PM",
                    arrivalTime: "06:45 AM (KLIA)",
                    duration: "5h 10m (Non-Stop)",
                    pnr: "CTWM-BOM-KLIA"
                }
            },

            cabTransfer: {
                pickupLocation: "KLIA Level 1 Door 4 Grab/Private Pickup",
                vehicle: "Toyota Vellfire Luxury MPV (W-9821-K)",
                driverName: "Azlan Shah",
                driverPhone: "+919742311023",
                durationToHotel: "40 mins via MEX Highway (54 km)"
            },

            hotelStay: {
                name: "The FACE Suites KL Skyline & Infinity Pool",
                address: "1020, Jalan Sultan Ismail, 50250 Kuala Lumpur",
                mapLink: "https://maps.google.com/?q=The+Face+Suites+KL",
                checkInTime: "12:00 PM (Infinity pool pass available from 08:00 AM)",
                checkOutTime: "11:00 AM",
                roomType: "1-Bedroom Deluxe Skyline Suite facing Petronas Towers",
                wifiSsid: "FaceSuites_HighSpeed",
                wifiPass: "klskyline2025",
                hostName: "Michelle Tan",
                hostPhone: "+919742311023"
            },

            days: [
                {
                    dayNumber: 1,
                    title: "Kuala Lumpur Skyline & Batu Caves",
                    summary: "Climb the 272 rainbow steps of Batu Caves, take the monorail to Bukit Bintang street feast.",
                    creatorSecretTip: "Visit Batu Caves at 7:30 AM before the sun heats up the limestone and tourists arrive.",
                    stops: [
                        {
                            id: "my_d1_s1",
                            name: "Batu Caves Rainbow Steps",
                            timing: "07:45 AM",
                            interStopTransit: "🚖 20 mins private transfer from The FACE Suites (12 km)",
                            category: "Temple Caves",
                            description: "Towering 140-foot golden Lord Murugan statue and 272 vibrant colored limestone steps.",
                            insiderTip: "Keep all snacks inside your backpack; the macaques are notorious pickpockets.",
                            photoUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
                            lat: 3.2379,
                            lng: 101.6840
                        }
                    ],
                    foodSpots: [
                        {
                            name: "Jalan Alor Hawker Street",
                            specialty: "Open-air Malaysian wok feast",
                            mustTryDish: "Char Kway Teow with Duck Egg & Satay",
                            approxCostForTwo: "45 MYR for two",
                            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
                            reelThumbnailUrl: "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80"
                        }
                    ]
                }
            ]
        }
    ],
    videoProofs: [
        {
            id: "v1",
            title: "ComeTripWithMe: Real Trips, Real Proof (Watch Before You Book)",
            destination: "Bengaluru, Delhi & Thailand",
            duration: "14:20",
            views: "45K views",
            thumbnailUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
            videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            highlights: ["Direct Airport Routes", "Pre-Booked Cabs", "Real street prices", "Local contacts"]
        },
        {
            id: "v2",
            title: "Gokarna: The Secret Beach Nobody Tells You About",
            destination: "Gokarna Coast",
            duration: "9:45",
            views: "32K views",
            thumbnailUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
            videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            highlights: ["Half Moon cliff trail", "₹300 boat negotiation", "Hidden natural rock pool"]
        },
        {
            id: "v3",
            title: "Himachal: The Riverside Mountain Café That Changed Everything",
            destination: "Parvati Valley",
            duration: "12:50",
            views: "58K views",
            thumbnailUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
            videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            highlights: ["Pine forest homestay", "Secret hot springs timing", "Trout fish preparation"]
        }
    ],
    instagramPosts: [
        {
            id: "ig1",
            handle: "@cometriipwme",
            channelType: "TRAVEL",
            caption: "The exact moment morning sun broke over Chapora Fort. 0 tourists, 100% ocean breeze. 📍 Goa",
            location: "Chapora Fort, North Goa",
            imageUrl: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80",
            likesCount: "1,840"
        },
        {
            id: "ig2",
            handle: "@cometriipwme",
            channelType: "TRAVEL",
            caption: "Phra Nang Cave beach right before the longtails arrived. Water clarity was unreal today. 🏝️",
            location: "Railay Peninsula, Krabi",
            imageUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
            likesCount: "2,410"
        },
        {
            id: "ig3",
            handle: "@beyondbengalurufoods",
            channelType: "FOOD",
            caption: "Piping hot butter garlic squid right by the shore. The crunch is everything. 🍜",
            location: "Anjuna Beach, Goa",
            imageUrl: "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&q=80",
            likesCount: "3,120"
        },
        {
            id: "ig4",
            handle: "@beyondbengalurufoods",
            channelType: "FOOD",
            caption: "Pad Kra Pao with duck egg cooked on a 40-year-old roaring wok in Bangkok Chinatown. 🔥",
            location: "Yaowarat, Bangkok",
            imageUrl: "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
            likesCount: "4,200"
        }
    ],
    reviews: [
        {
            id: "r1",
            authorHandle: "@rohini.explores",
            city: "Bengaluru",
            tripTag: "🛫 BLR ➔ GOX North Goa Circuit",
            rating: 5,
            reviewQuote: "Landed at Mopa airport, cab was right at Gate 3 as promised. Checked into Thalassa villa and didn't have to negotiate a single auto. Truly 10/10."
        },
        {
            id: "r2",
            authorHandle: "@arjun_wanders",
            city: "Delhi",
            tripTag: "🛫 DEL ➔ BKK Thailand & Krabi",
            rating: 5,
            reviewQuote: "Departed from T3 Delhi. Every single transfer, ferry from Ao Nang to Railay, and Chinatown street food wok matched the video proof perfectly."
        },
        {
            id: "r3",
            authorHandle: "@priya.irl",
            city: "Mumbai",
            tripTag: "🛫 BOM ➔ KUU Himachal Valley",
            rating: 5,
            reviewQuote: "Booked from Mumbai with connecting flight to Chandigarh. The 4x4 cab picked us up and dropped us at the Chalal bridge. Super smooth experience."
        }
    ],
    packingItems: [
        { id: "p1", title: "Valid Govt ID / Passport & Flight Ticket", category: "Essentials", isChecked: true },
        { id: "p2", title: "Power Bank (min 10,000 mAh for flights)", category: "Tech", isChecked: false },
        { id: "p3", title: "Comfortable flight sneakers & sandals", category: "Apparel", isChecked: false },
        { id: "p4", title: "Sunscreen SPF 50+ & Sunglasses", category: "Care", isChecked: true },
        { id: "p5", title: "Quick-dry beach towel & Swimwear", category: "Apparel", isChecked: false },
        { id: "p6", title: "Offline downloaded maps & playlist", category: "Tech", isChecked: false }
    ],
    wishlist: ["goa", "thailand"]
};

// State Manager
class AppStore {
    constructor() {
        const saved = localStorage.getItem('cometrip_store_data_v3');
        if (saved) {
            try {
                this.data = JSON.parse(saved);
            } catch(e) {
                this.data = JSON.parse(JSON.stringify(FACTORY_DATA));
            }
        } else {
            this.data = JSON.parse(JSON.stringify(FACTORY_DATA));
        }

        this.selectedOrigin = this.data.userBooking.departureOrigin || 'BLR';
        this.selectedAirportFilter = 'ALL';
        this.activeTab = 'explore';
        this.activeGuideTripId = 'goa';
        this.activeGuideDayIndex = 0;
        this.timelineScrubIndex = 0;
        this.visitedStops = new Set();
        this.activeAudioStory = null;
        this.isPlayingAudio = false;
        this.speechRate = 1.0;
        this.speechUtterance = null;
        this.selectedVibe = 'ALL';
        this.selectedReelsChannel = 'ALL';
    }

    save() {
        localStorage.setItem('cometrip_store_data_v3', JSON.stringify(this.data));
    }

    getTrip(id) {
        return this.data.trips.find(t => t.id.toLowerCase() === id.toLowerCase()) || this.data.trips[0];
    }

    getOriginRoute(trip, originCode = null) {
        const org = originCode || this.selectedOrigin;
        if (trip.originRoutes && trip.originRoutes[org]) {
            return trip.originRoutes[org];
        }
        return trip.originRoutes ? (trip.originRoutes['BLR'] || Object.values(trip.originRoutes)[0]) : null;
    }

    toggleWishlist(tripId) {
        const idx = this.data.wishlist.indexOf(tripId);
        if (idx >= 0) {
            this.data.wishlist.splice(idx, 1);
            showToast("Removed from wishlist ♡");
        } else {
            this.data.wishlist.push(tripId);
            showToast("Added to wishlist ✦");
        }
        this.save();
        renderExploreTrips();
        renderWishlist();
    }

    isWishlisted(tripId) {
        return this.data.wishlist.includes(tripId);
    }
}

const store = new AppStore();

// Set Departure Origin City (BLR / DEL / BOM)
function setGlobalOriginCity(originCode) {
    store.selectedOrigin = originCode;
    store.data.userBooking.departureOrigin = originCode;
    store.save();

    // Update Header Buttons
    document.querySelectorAll('.origin-city-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.getElementById('originBtn-' + originCode);
    if (activeBtn) activeBtn.classList.add('active');

    // Update Hero Tag & Spotlights
    const org = store.data.origins[originCode] || store.data.origins['BLR'];
    const heroTag = document.getElementById('heroOriginTag');
    if (heroTag) heroTag.textContent = `✦ DEPARTING FROM ${org.name.toUpperCase()} (${org.code}) · AIRPORT MAPPED`;
    
    const spotOrigin = document.getElementById('spotlightOriginName');
    if (spotOrigin) spotOrigin.textContent = `${org.name} (${org.code})`;

    // Update Dropdown in Smart Match & Planner
    const smartSelect = document.getElementById('smartOriginSelect');
    if (smartSelect) smartSelect.value = originCode;

    const plannerRadios = document.querySelectorAll('input[name="plannerFromCity"]');
    plannerRadios.forEach(r => {
        if (r.value.includes(originCode)) r.checked = true;
    });

    renderExploreTrips();
    runSmartMatch();
    if (store.activeTab === 'guide') renderPocketGuide();

    showToast(`🛫 Departure City set to ${org.name} (${org.code})`);
}

// Viewport / Screen Controls
function toggleViewportMode(mode) {
    const wrapper = document.getElementById('viewportWrapper');
    const btnMob = document.getElementById('btnViewMobile');
    const btnDesk = document.getElementById('btnViewDesktop');

    if (mode === 'desktop') {
        wrapper.classList.add('fullscreen-mode');
        btnDesk.classList.add('active');
        btnMob.classList.remove('active');
    } else {
        wrapper.classList.remove('fullscreen-mode');
        btnMob.classList.add('active');
        btnDesk.classList.remove('active');
    }
}

function toggleCmsDrawer() {
    const drawer = document.getElementById('cmsDrawer');
    drawer.classList.toggle('open');
    const btn = document.getElementById('btnCmsTrigger');
    btn.classList.toggle('active');
    if (drawer.classList.contains('open')) {
        populateCmsFields();
    }
}

// Navigation Tabs
function switchTab(tabId) {
    store.activeTab = tabId;
    
    document.querySelectorAll('.nav-item-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    const activeNav = document.getElementById('navBtn-' + tabId);
    if (activeNav) activeNav.classList.add('active');

    document.querySelectorAll('.screen-view').forEach(screen => {
        screen.classList.remove('active-screen');
    });
    const activeScreen = document.getElementById('screen-' + tabId);
    if (activeScreen) {
        activeScreen.classList.add('active-screen');
    }

    document.getElementById('appMainScroll').scrollTo({ top: 0, behavior: 'smooth' });

    if (tabId === 'guide') {
        renderPocketGuide();
    } else if (tabId === 'saved') {
        renderWishlist();
        renderPackingList();
    }
}

// RENDER: EXPLORE SCREEN WITH AIRPORT GATEWAYS
function renderExploreScreen() {
    const spotContainer = document.getElementById('spotlightsContainer');
    spotContainer.innerHTML = store.data.spotlights.map(s => `
        <div class="spotlight-card" onclick="viewSpotlight('${s.id}')">
            <img src="${s.imageUrl}" class="spotlight-img" alt="${s.title}">
            <div class="spotlight-overlay">
                <span class="spotlight-region">${s.region}</span>
                <h4 class="spotlight-name">${s.title}</h4>
            </div>
        </div>
    `).join('');

    renderExploreTrips();
    runSmartMatch();
}

function renderExploreTrips() {
    const container = document.getElementById('tripsGridContainer');
    
    let filtered = store.data.trips;
    if (store.selectedAirportFilter !== 'ALL') {
        filtered = filtered.filter(t => t.airportInfo && (t.airportInfo.primaryCode === store.selectedAirportFilter || t.airportInfo.alternateCode === store.selectedAirportFilter));
    }
    if (store.selectedVibe !== 'ALL') {
        filtered = filtered.filter(t => t.vibe === store.selectedVibe);
    }

    container.innerHTML = filtered.map(t => {
        const isSaved = store.isWishlisted(t.id);
        const route = store.getOriginRoute(t);
        const ap = t.airportInfo;

        return `
            <div class="trip-card" onclick="openTripDetailModal('${t.id}')">
                <div class="trip-card-image-wrap">
                    <img src="${t.imageUrl}" class="trip-card-image" alt="${t.name}">
                    <div class="trip-card-overlay-top">
                        <span class="airport-hub-badge"><i class="fa-solid fa-plane-arrival"></i> ${ap ? ap.primaryCode : 'AIR'}</span>
                        <button class="wishlist-heart-btn ${isSaved ? 'is-saved' : ''}" onclick="event.stopPropagation(); store.toggleWishlist('${t.id}')">
                            <i class="fa-${isSaved ? 'solid' : 'regular'} fa-heart"></i>
                        </button>
                    </div>
                    <div class="trip-card-overlay-bottom">
                        <span class="trip-price-pill">${t.price}</span>
                        <span class="trip-duration-pill">${t.duration}</span>
                    </div>
                </div>
                <div class="trip-card-body">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <h3 class="trip-card-title">${t.name}</h3>
                        <span class="vibe-badge vibe-${t.vibe.toLowerCase()}" style="font-size:9px;">${getVibeEmoji(t.vibe)} ${t.vibe}</span>
                    </div>
                    
                    <div class="trip-card-headline">${t.headline}</div>
                    
                    <!-- Real-Time Airport Route Pill -->
                    ${route ? `
                        <div style="background:rgba(56, 189, 248, 0.12); border:1px solid rgba(56, 189, 248, 0.3); border-radius:var(--radius-md); padding:6px 10px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:10px; color:#7DD3FC; font-weight:800;">
                                <i class="fa-solid fa-plane"></i> ${route.originCode} ➔ ${ap ? ap.primaryCode : 'DEST'}
                            </span>
                            <span style="font-size:10px; color:var(--text-muted);">${route.duration}</span>
                        </div>
                    ` : ''}

                    <p class="trip-card-desc">${t.description}</p>
                    <div class="trip-card-tags">
                        ${t.heroTags.map(tag => `<span class="tag-pill">${tag}</span>`).join('')}
                    </div>
                    <div class="trip-card-footer">
                        <span style="font-size:11px; color:var(--gold-primary); font-weight:700;">✦ Direct Airport Route</span>
                        <span class="gold-btn" style="padding:6px 14px; font-size:11px;">View Flight & Stay ➔</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getVibeEmoji(vibe) {
    switch(vibe) {
        case 'PARTY': return '🎉';
        case 'BACKPACKING': return '🎒';
        case 'CHILL': return '🏔️';
        case 'LUXURY': return '✨';
        case 'HERITAGE': return '🏛️';
        default: return '✦';
    }
}

function filterTripsByAirport(code, btn) {
    store.selectedAirportFilter = code;
    document.querySelectorAll('#airportFilterChips .filter-chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderExploreTrips();
}

function filterTripsByVibe(vibe, btn) {
    store.selectedVibe = vibe;
    renderExploreTrips();
}

function viewSpotlight(id) {
    const matched = store.data.trips.find(t => t.id.includes(id) || id.includes(t.id));
    if (matched) {
        openTripDetailModal(matched.id);
    } else {
        openTripDetailModal(store.data.trips[0].id);
    }
}

// Smart Match Engine
function updateBudgetSliderVal(val) {
    document.getElementById('smartBudgetVal').textContent = '₹' + parseInt(val).toLocaleString('en-IN');
    runSmartMatch();
}

function runSmartMatch() {
    const dest = document.getElementById('smartDestSelect').value;
    const org = store.selectedOrigin;
    const orgData = store.data.origins[org] || store.data.origins['BLR'];

    let recTitle = "Direct Flight & Curated Circuit";
    let recSub = `Handcrafted route departing from ${orgData.name} (${orgData.code}) with airport pickup and boutique stay.`;

    if (dest === 'goa') {
        recTitle = `✦ ${orgData.code} ➔ GOX Goa Long Weekend — ₹8,999/person`;
        recSub = `Direct route from ${orgData.name}. 3 nights North & South Goa, Thalassa sunset table & pre-booked airport cab.`;
    } else if (dest === 'thailand') {
        recTitle = `✦ ${orgData.code} ➔ BKK Bangkok + Krabi Islands — ₹24,999`;
        recSub = `International connection from ${orgData.name}. 7 nights Chinatown street food, longtails & Railay beach.`;
    } else if (dest === 'himachal') {
        recTitle = `✦ ${orgData.code} ➔ KUU Parvati Valley Kasol — ₹11,999`;
        recSub = `Scenic connection from ${orgData.name}. 5 nights riverside cedar wood cottage & Kheerganga hot springs.`;
    } else if (dest === 'gokarna') {
        recTitle = `✦ ${orgData.code} ➔ HBX Gokarna Beach Trail — ₹6,499`;
        recSub = `Coastal route from ${orgData.name}. 4 nights Kudle sunset huts & Half Moon cliff trek.`;
    } else if (dest === 'pondicherry') {
        recTitle = `✦ ${orgData.code} ➔ MAA Pondicherry French Qtr — ₹5,499`;
        recSub = `Flight/Sleeper from ${orgData.name} + ECR highway cab. 3 nights French heritage villa & vintage cycle crawl.`;
    }

    document.getElementById('smartResultTitle').textContent = recTitle;
    document.getElementById('smartResultSub').textContent = recSub;
}

function viewSmartMatchedTrip() {
    const dest = document.getElementById('smartDestSelect').value;
    openTripDetailModal(dest);
}

function inquireSmartMatchWhatsApp() {
    const dest = document.getElementById('smartDestSelect').value;
    const org = store.selectedOrigin;
    const budget = document.getElementById('smartBudgetVal').textContent;
    const title = document.getElementById('smartResultTitle').textContent;

    const msg = `Hey ComeTripWithMe! ✦ I'm interested in the airport-mapped trip:\n\n` +
                `🛫 Departing Airport: ${org} (${store.data.origins[org].name})\n` +
                `📍 Destination: ${dest.toUpperCase()}\n` +
                `💰 Budget: ${budget}/person\n` +
                `📋 Selected Route: ${title}\n\n` +
                `Can you confirm flight boarding slots and available dates?`;

    openWhatsAppLink(msg);
}

// TRIP DETAIL MODAL WITH MULTI-ORIGIN (BLR / DEL / BOM)
function openTripDetailModal(tripId) {
    const trip = store.getTrip(tripId);
    if (!trip) return;

    document.getElementById('modalTripName').textContent = trip.name;
    const body = document.getElementById('modalTripBody');
    const isSaved = store.isWishlisted(trip.id);
    const ap = trip.airportInfo;
    const route = store.getOriginRoute(trip);

    body.innerHTML = `
        <div style="width:100%; height:200px; border-radius:var(--radius-lg); overflow:hidden; position:relative; margin-bottom:16px;">
            <img src="${trip.imageUrl}" style="width:100%; height:100%; object-fit:cover;" alt="${trip.name}">
            <div style="position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(7,9,14,0.9) 100%); padding:16px; display:flex; flex-direction:column; justify-content:flex-end;">
                <div style="display:flex; gap:6px; margin-bottom:4px;">
                    <span class="airport-hub-badge"><i class="fa-solid fa-plane-arrival"></i> ${ap ? ap.primaryCode : 'DEST'} Gateway</span>
                    <span class="vibe-badge vibe-${trip.vibe.toLowerCase()}">${getVibeEmoji(trip.vibe)} ${trip.vibe}</span>
                </div>
                <h2 style="font-family:var(--font-heading); font-size:20px; font-weight:900; color:#fff;">${trip.headline}</h2>
            </div>
        </div>

        <!-- Origin Selector Tabs inside Trip Modal -->
        <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:10px 14px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11px; font-weight:800; color:var(--gold-light);"><i class="fa-solid fa-plane-departure"></i> Select Your Origin:</span>
            <div style="display:flex; gap:4px;">
                <button class="origin-city-btn ${store.selectedOrigin === 'BLR' ? 'active' : ''}" onclick="setGlobalOriginCity('BLR'); openTripDetailModal('${trip.id}')">BLR</button>
                <button class="origin-city-btn ${store.selectedOrigin === 'DEL' ? 'active' : ''}" onclick="setGlobalOriginCity('DEL'); openTripDetailModal('${trip.id}')">DEL</button>
                <button class="origin-city-btn ${store.selectedOrigin === 'BOM' ? 'active' : ''}" onclick="setGlobalOriginCity('BOM'); openTripDetailModal('${trip.id}')">BOM</button>
            </div>
        </div>

        <!-- Flight & Departure Hub Card -->
        ${route ? `
            <div class="transit-hub-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span class="transit-badge"><i class="fa-solid fa-plane"></i> ${route.originCode} ➔ ${ap ? ap.primaryCode : 'DEST'} Flight Logistics</span>
                    <span style="font-family:var(--font-mono); font-size:11px; color:#7DD3FC;">PNR: ${route.pnr}</span>
                </div>
                
                <div class="ticket-meta-grid" style="margin-bottom:12px;">
                    <div>
                        <div class="ticket-label">Departure Airport & Terminal</div>
                        <div class="ticket-val" style="font-size:12px;">${route.terminal}</div>
                        <div style="font-size:11px; color:var(--gold-light); font-weight:700;">📍 Gate: ${route.gate}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Flight Timings & Duration</div>
                        <div class="ticket-val" style="font-size:12px;">🛫 Dep: ${route.departureTime}</div>
                        <div style="font-size:11px; color:#86EFAC;">🛬 Arr: ${route.arrivalTime} (${route.duration})</div>
                    </div>
                </div>

                <div style="border-top:1px solid rgba(56, 189, 248, 0.2); padding-top:10px; margin-top:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-size:11px; font-weight:800; color:#fff;"><i class="fa-solid fa-taxi" style="color:var(--gold-primary); margin-right:6px;"></i> Airport Cab Pickup at ${ap ? ap.primaryCode : 'Airport'}</span>
                        <span style="font-size:10px; color:#86EFAC; font-weight:700;">Pick-up: ${trip.cabTransfer.pickupLocation}</span>
                    </div>
                    <div style="font-size:11px; color:var(--text-secondary); line-height:1.4;">
                        🚖 <strong>Vehicle:</strong> ${trip.cabTransfer.vehicle} · Driver: ${trip.cabTransfer.driverName} (${trip.cabTransfer.durationToHotel})
                    </div>
                </div>
            </div>

            <!-- Hotel & Stay Location Box -->
            <div class="hotel-hub-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span class="hotel-badge"><i class="fa-solid fa-hotel"></i> Stay Location & Check-in</span>
                    <span style="font-size:11px; color:#D8B4FE; font-weight:700;">Check-in: ${trip.hotelStay.checkInTime}</span>
                </div>
                <h4 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff; margin-bottom:4px;">${trip.hotelStay.name}</h4>
                <p style="font-size:11px; color:var(--text-secondary); margin-bottom:8px;">📍 ${trip.hotelStay.address}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.3); padding:8px 12px; border-radius:var(--radius-md);">
                    <span style="font-size:10px; color:var(--text-muted);"><i class="fa-solid fa-wifi" style="color:#D8B4FE;"></i> WiFi: <strong>${trip.hotelStay.wifiSsid}</strong></span>
                    <a href="${trip.hotelStay.mapLink}" target="_blank" class="gold-badge" style="font-size:9px; text-decoration:none;">
                        <i class="fa-solid fa-location-arrow"></i> Navigate
                    </a>
                </div>
            </div>
        ` : ''}

        <!-- Creator Note -->
        <div class="insider-tip-box" style="margin-bottom:18px;">
            <strong>✦ Creator Field Note:</strong> ${trip.creatorNote}
        </div>

        <!-- Day-by-Day Breakdown -->
        <h3 class="section-title" style="margin-bottom:12px;"><span class="sparkle">✦</span> Day-by-Day Itinerary</h3>
        <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:20px;">
            ${trip.days.map(d => `
                <div class="glass-panel" style="padding:14px; margin-bottom:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-size:12px; font-weight:800; color:var(--gold-light);">Day ${d.dayNumber}: ${d.title}</span>
                        <span class="gold-badge" style="font-size:10px;">${d.stops.length} Stops</span>
                    </div>
                    <p style="font-size:11px; color:var(--text-secondary); line-height:1.4; margin-bottom:10px;">${d.summary}</p>
                    
                    <div style="display:flex; flex-direction:column; gap:8px;">
                        ${d.stops.map(s => `
                            <div>
                                ${s.interStopTransit ? `
                                    <div class="inter-stop-transit-pill">
                                        <i class="fa-solid fa-route"></i> ${s.interStopTransit}
                                    </div>
                                ` : ''}
                                <div style="background:var(--bg-dark); border:1px solid var(--glass-border-subtle); border-radius:var(--radius-md); padding:10px; display:flex; justify-content:space-between; align-items:center;">
                                    <div>
                                        <div style="font-size:12px; font-weight:700; color:#fff;">📍 ${s.name}</div>
                                        <div style="font-size:10px; color:var(--gold-primary);">${s.timing} · ${s.category}</div>
                                    </div>
                                    ${s.audioStory ? `<span class="gold-badge" style="font-size:9px;"><i class="fa-solid fa-headphones"></i> Audio</span>` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        </div>

        <!-- Booking Actions -->
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button class="gold-btn" style="flex:1;" onclick="bookTripAndActivateLivePass('${trip.id}')">
                <i class="fa-solid fa-ticket"></i> Book from ${store.selectedOrigin} & Activate Pass
            </button>
            <button class="glass-btn" onclick="store.toggleWishlist('${trip.id}'); openTripDetailModal('${trip.id}');">
                <i class="fa-${isSaved ? 'solid' : 'regular'} fa-heart" style="${isSaved ? 'color:#FF5A5F' : ''}"></i> ${isSaved ? 'Wishlisted' : 'Wishlist'}
            </button>
        </div>
    `;

    document.getElementById('modalStartGuideBtn').onclick = () => {
        closeModal('tripDetailModal');
        bookTripAndActivateLivePass(trip.id);
    };

    openModal('tripDetailModal');
}

// REAL-TIME DIGITAL BOARDING PASS WITH MULTI-ORIGIN
function bookTripAndActivateLivePass(tripId) {
    const trip = store.getTrip(tripId);
    store.data.userBooking.bookedTripId = trip.id;
    store.data.userBooking.departureOrigin = store.selectedOrigin;
    store.data.userBooking.bookingId = `CTWM-${store.selectedOrigin}-${trip.id.toUpperCase()}-${Math.floor(1000 + Math.random() * 9000)}`;
    store.save();
    
    closeModal('tripDetailModal');
    showToast(`🎉 Trip Booked from ${store.selectedOrigin}! Live Boarding Pass Generated ✦`);
    openActiveBoardingPassModal();
}

function openActiveBoardingPassModal() {
    const b = store.data.userBooking;
    const trip = store.getTrip(b.bookedTripId || 'goa');
    const org = store.selectedOrigin || b.departureOrigin || 'BLR';
    const route = store.getOriginRoute(trip, org);
    const ap = trip.airportInfo;

    document.getElementById('passModalTripName').textContent = trip.name;
    const body = document.getElementById('passModalBody');

    body.innerHTML = `
        <div class="boarding-pass-card">
            <div class="boarding-pass-header">
                <div>
                    <span style="font-size:9px; font-weight:900; letter-spacing:1px; text-transform:uppercase;">OFFICIAL BOARDING PASS · ${org} ➔ ${ap ? ap.primaryCode : 'DEST'}</span>
                    <h3 style="font-family:var(--font-heading); font-size:18px; font-weight:900;">${trip.name.toUpperCase()}</h3>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:10px; font-weight:700;">PASSENGER</span>
                    <div style="font-weight:900; font-size:13px;">${b.passengerName}</div>
                </div>
            </div>

            <div class="boarding-pass-body">
                <div class="ticket-meta-grid">
                    <div>
                        <div class="ticket-label">Flight Route</div>
                        <div class="ticket-val mono" style="font-size:14px; color:#38BDF8;">${org} ➔ ${ap ? ap.primaryCode : 'DEST'}</div>
                        <div style="font-size:10px; color:var(--text-muted);">${route ? route.transport : 'Flight'}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Booking Reference / PNR</div>
                        <div class="ticket-val mono">${route ? route.pnr : b.bookingId}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Departure Terminal & Gate</div>
                        <div class="ticket-val">${route ? route.terminal : 'Terminal 2'}</div>
                        <div style="font-size:11px; color:var(--gold-light); font-weight:700;">📍 Gate: ${route ? route.gate : '14B'}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Boarding & Departure Time</div>
                        <div class="ticket-val" style="color:var(--gold-light);">Board: ${route ? route.boardingTime : '05:45 AM'}</div>
                        <div style="font-size:11px; color:#86EFAC;">🛫 Dep: ${route ? route.departureTime : '06:30 AM'}</div>
                    </div>
                </div>

                <div class="ticket-perforated-divider"></div>

                <!-- Cab & Hotel Live Vouchers -->
                <div style="display:flex; flex-direction:column; gap:10px;">
                    <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-size:11px; font-weight:800; color:#7DD3FC;"><i class="fa-solid fa-taxi"></i> Airport Pickup at ${ap ? ap.primaryCode : 'Arrival'}</span>
                            <span style="font-size:10px; color:var(--gold-light); font-weight:700;">ETA: ${route ? route.arrivalTime : '08:00 AM'}</span>
                        </div>
                        <div style="font-size:11px; color:var(--text-secondary);">
                            📍 ${trip.cabTransfer.pickupLocation}<br>
                            🚖 ${trip.cabTransfer.vehicle} · 📞 Driver: ${trip.cabTransfer.driverName}
                        </div>
                    </div>

                    <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-size:11px; font-weight:800; color:#D8B4FE;"><i class="fa-solid fa-hotel"></i> Resort Stay & Check-in</span>
                            <span style="font-size:10px; color:#D8B4FE; font-weight:700;">Check-in: ${trip.hotelStay.checkInTime}</span>
                        </div>
                        <div style="font-size:11px; color:var(--text-secondary);">
                            🏨 ${trip.hotelStay.name}<br>
                            📍 ${trip.hotelStay.address}<br>
                            🔑 WiFi: <strong>${trip.hotelStay.wifiSsid}</strong> (${trip.hotelStay.wifiPass})
                        </div>
                    </div>
                </div>

                <!-- Barcode -->
                <div style="margin-top:16px; text-align:center;">
                    <div style="font-family:var(--font-mono); font-size:24px; letter-spacing:4px; color:var(--gold-primary);">|||| | ||||| || |||||| | |||</div>
                    <div style="font-size:9px; color:var(--text-muted); letter-spacing:1px; margin-top:2px;">VALID AT ${org} AIRPORT SECURITY & RESORT RECEPTION</div>
                </div>
            </div>
        </div>

        <div style="display:flex; gap:10px;">
            <button class="gold-btn" style="flex:1;" onclick="closeModal('boardingPassModal'); startLiveGuideForTrip('${trip.id}');">
                <i class="fa-solid fa-route"></i> Open Live Interactive Pocket Guide
            </button>
            <button class="glass-btn" onclick="inquireTripWhatsApp('${trip.id}')">
                <i class="fa-brands fa-whatsapp"></i> Contact Host
            </button>
        </div>
    `;

    openModal('boardingPassModal');
}

// RENDER: POCKET GUIDE SCREEN
function renderPocketGuide() {
    const trip = store.getTrip(store.activeGuideTripId);
    document.getElementById('guideActiveTripTitle').textContent = trip.name;

    const dropdown = document.getElementById('guideTripDropdown');
    dropdown.innerHTML = store.data.trips.map(t => `
        <option value="${t.id}" ${t.id === trip.id ? 'selected' : ''}>${t.name}</option>
    `).join('');

    const transitHub = document.getElementById('guideTransitHubSection');
    const route = store.getOriginRoute(trip);
    const ap = trip.airportInfo;

    if (route) {
        transitHub.innerHTML = `
            <div class="transit-hub-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="transit-badge"><i class="fa-solid fa-plane-departure"></i> ${route.originCode} ➔ ${ap ? ap.primaryCode : 'DEST'} Flight Logistics</span>
                    <span style="font-size:10px; color:#86EFAC; font-weight:700;">Boarding: ${route.boardingTime}</span>
                </div>
                <div style="font-size:12px; font-weight:800; color:#fff;">${route.transport} · ${route.terminal}</div>
                <div style="font-size:11px; color:var(--gold-light); margin-top:2px;">📍 <strong>Boarding Gate:</strong> ${route.gate} (Dep: ${route.departureTime})</div>
                <div style="font-size:11px; color:var(--text-secondary); margin-top:4px;">🛬 <strong>Landing at:</strong> ${ap ? ap.primaryName : 'Destination'} at ${route.arrivalTime} (${ap ? ap.baggageCarousel : 'Belt 1'})</div>
            </div>

            <div class="hotel-hub-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="hotel-badge"><i class="fa-solid fa-taxi"></i> Cab Pick-up & Resort Stay</span>
                    <span style="font-size:10px; color:#D8B4FE; font-weight:700;">ETA: ${route.arrivalTime}</span>
                </div>
                <div style="font-size:12px; font-weight:800; color:#fff;">🚖 ${trip.cabTransfer.pickupLocation}</div>
                <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">${trip.cabTransfer.vehicle} · Driver: <strong>${trip.cabTransfer.driverName}</strong> (${trip.cabTransfer.durationToHotel})</div>
                
                <div style="border-top:1px solid rgba(168, 85, 247, 0.2); padding-top:8px; margin-top:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:12px; font-weight:800; color:#fff;">🏨 ${trip.hotelStay.name}</div>
                        <div style="font-size:10px; color:var(--text-muted);">Check-in: ${trip.hotelStay.checkInTime} · WiFi: ${trip.hotelStay.wifiSsid}</div>
                    </div>
                    <a href="${trip.hotelStay.mapLink}" target="_blank" class="gold-badge" style="font-size:9px; text-decoration:none;">
                        <i class="fa-solid fa-location-arrow"></i> Map
                    </a>
                </div>
            </div>
        `;
    } else {
        transitHub.innerHTML = '';
    }

    // Day Tabs
    const dayTabsContainer = document.getElementById('guideDayTabsContainer');
    dayTabsContainer.innerHTML = trip.days.map((d, idx) => `
        <button class="guide-day-pill ${idx === store.activeGuideDayIndex ? 'active' : ''}" onclick="switchGuideDay(${idx})">
            Day ${d.dayNumber}
        </button>
    `).join('');

    const currentDay = trip.days[store.activeGuideDayIndex] || trip.days[0];
    document.getElementById('guideDayTitle').textContent = `Day ${currentDay.dayNumber}: ${currentDay.title}`;
    document.getElementById('guideDaySummary').textContent = currentDay.summary;
    document.getElementById('guideCreatorSecretTip').innerHTML = `<strong>✦ Creator Secret Tip:</strong> ${currentDay.creatorSecretTip}`;

    const totalStops = currentDay.stops.length;
    let visitedCount = 0;
    currentDay.stops.forEach(s => {
        if (store.visitedStops.has(s.id)) visitedCount++;
    });
    document.getElementById('guideProgressCounter').textContent = `${visitedCount} / ${totalStops} Visited`;
    const pct = totalStops > 0 ? (visitedCount / totalStops) * 100 : 0;
    document.getElementById('guideProgressFill').style.width = pct + '%';

    renderRouteMapSvg(currentDay);

    const stopsContainer = document.getElementById('guideStopsContainer');
    stopsContainer.innerHTML = currentDay.stops.map((s, idx) => {
        const isVisited = store.visitedStops.has(s.id);
        return `
            <div>
                ${s.interStopTransit ? `
                    <div class="inter-stop-transit-pill">
                        <i class="fa-solid fa-route"></i> ${s.interStopTransit}
                    </div>
                ` : ''}
                <div class="stop-timeline-item">
                    <div class="stop-dot-marker ${isVisited ? 'visited' : ''}" onclick="toggleStopVisited('${s.id}')">
                        ${isVisited ? '<i class="fa-solid fa-check"></i>' : (idx + 1)}
                    </div>
                    <div class="stop-card">
                        <div class="stop-card-header">
                            <div>
                                <h4 class="stop-name">${s.name}</h4>
                                <span style="font-size:11px; color:var(--text-muted);">${s.category}</span>
                            </div>
                            <span class="stop-time-badge">${s.timing}</span>
                        </div>

                        ${s.photoUrl ? `<img src="${s.photoUrl}" class="stop-img-preview" alt="${s.name}">` : ''}

                        <p style="font-size:12px; color:var(--text-secondary); line-height:1.45; margin-bottom:8px;">${s.description}</p>

                        <div class="insider-tip-box">
                            <strong>✦ Insider Tip:</strong> ${s.insiderTip}
                        </div>

                        <div class="stop-actions-row">
                            <label style="display:flex; align-items:center; gap:6px; font-size:11px; color:var(--text-secondary); cursor:pointer;">
                                <input type="checkbox" ${isVisited ? 'checked' : ''} onchange="toggleStopVisited('${s.id}')">
                                <span>Mark Visited</span>
                            </label>
                            <div style="display:flex; gap:8px;">
                                ${s.audioStory ? `
                                    <button class="gold-btn" style="padding:6px 12px; font-size:11px;" onclick="playAudioStory('${trip.id}', ${store.activeGuideDayIndex}, '${s.id}')">
                                        <i class="fa-solid fa-headphones"></i> Listen ✦
                                    </button>
                                ` : ''}
                                <a href="https://maps.google.com/?q=${s.lat || 15.6},${s.lng || 73.7}" target="_blank" class="glass-btn" style="padding:6px 10px; font-size:11px;">
                                    <i class="fa-solid fa-location-arrow"></i> Map
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    const foodContainer = document.getElementById('guideFoodSpotsContainer');
    foodContainer.innerHTML = currentDay.foodSpots.map(f => `
        <div class="glass-panel" style="padding:14px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                <div>
                    <h4 style="font-family:var(--font-heading); font-size:14px; font-weight:800; color:#fff;">🍜 ${f.name}</h4>
                    <span style="font-size:11px; color:var(--gold-primary); font-weight:600;">${f.specialty}</span>
                </div>
                <span class="gold-badge" style="font-size:10px;">${f.approxCostForTwo}</span>
            </div>
            <div style="font-size:11px; color:var(--text-secondary); margin-bottom:10px;">
                <strong>Must Order:</strong> ${f.mustTryDish}
            </div>
            <div style="display:flex; justify-content:flex-end;">
                <a href="${f.reelUrl}" target="_blank" class="glass-btn" style="padding:6px 12px; font-size:11px;">
                    <i class="fa-brands fa-instagram" style="color:#E1306C;"></i> Watch Food Review Reel
                </a>
            </div>
        </div>
    `).join('');
}

function switchGuideTrip(tripId) {
    store.activeGuideTripId = tripId;
    store.activeGuideDayIndex = 0;
    renderPocketGuide();
}

function switchGuideDay(dayIndex) {
    store.activeGuideDayIndex = dayIndex;
    renderPocketGuide();
}

function startLiveGuideForTrip(tripId) {
    store.activeGuideTripId = tripId;
    store.activeGuideDayIndex = 0;
    switchTab('guide');
    showToast(`✦ Pocket Guide active for ${store.getTrip(tripId).name}`);
}

function toggleStopVisited(stopId) {
    if (store.visitedStops.has(stopId)) {
        store.visitedStops.delete(stopId);
    } else {
        store.visitedStops.add(stopId);
        showToast("✓ Stop marked visited!");
    }
    renderPocketGuide();
}

function scrubTimelineStage(val) {
    store.timelineScrubIndex = parseInt(val);
    const org = store.selectedOrigin;
    const trip = store.getTrip(store.activeGuideTripId);
    const route = store.getOriginRoute(trip);
    const ap = trip.airportInfo;

    const stages = [
        { pill: `🟢 LIVE · FLIGHT BOARDING AT ${org}`, time: route ? route.boardingTime : "05:45 AM", title: `✈️ ${route ? route.terminal : org} · ${route ? route.transport : 'Flight'}`, desc: `Gate ${route ? route.gate : '14B'} boarding in progress. Filter coffee pitstop before takeoff.` },
        { pill: `🛬 LIVE · LANDING AT ${ap ? ap.primaryCode : 'DEST'} AIRPORT`, time: route ? route.arrivalTime : "07:45 AM", title: `🛬 ${ap ? ap.primaryName : 'Airport'} Terminal Arrival`, desc: `Flight landed safely. Head to Baggage Carousel ${ap ? ap.baggageCarousel : 'Belt 3'}.` },
        { pill: "🚖 LIVE · CAB PICK-UP EN ROUTE TO RESORT", time: "08:15 AM", title: `🚖 Cab Pick-up at ${trip.cabTransfer.pickupLocation}`, desc: `Driver ${trip.cabTransfer.driverName} waiting in ${trip.cabTransfer.vehicle}. ${trip.cabTransfer.durationToHotel}.` },
        { pill: "🏨 LIVE · RESORT CHECK-IN & WELCOME DRINK", time: trip.hotelStay.checkInTime, title: `🏨 ${trip.hotelStay.name} Check-in`, desc: `Keys & scooty handed over at reception. WiFi: ${trip.hotelStay.wifiSsid}` },
        { pill: "🌅 LIVE · EVENING CLIFF SUNDOWNER", time: "05:30 PM", title: "🌅 Golden Hour Sunset & Creator Food Trail", desc: "Golden hour sunset light over the bay. Reserved table ready." }
    ];

    const current = stages[store.timelineScrubIndex] || stages[0];
    document.getElementById('hudLivePill').textContent = current.pill;
    document.getElementById('hudSimTime').textContent = current.time;
    document.getElementById('hudStageTitle').textContent = current.title;
    document.getElementById('hudStageDesc').textContent = current.desc;
}

function renderRouteMapSvg(currentDay) {
    const svg = document.getElementById('routeMapSvg');
    const stops = currentDay.stops;
    if (!stops || stops.length === 0) return;
    const org = store.selectedOrigin;
    const trip = store.getTrip(store.activeGuideTripId);
    const ap = trip.airportInfo;

    const points = [
        { x: 30, y: 40, name: `✈️ ${org} Dep`, icon: "plane" },
        { x: 95, y: 135, name: `🛬 ${ap ? ap.primaryCode : 'Arr'}`, icon: "plane" },
        { x: 165, y: 65, name: "🏨 Resort", icon: "hotel" },
        ...stops.map((s, i) => ({
            x: 230 + (i * 75),
            y: 90 + (Math.sin(i * 2) * 40),
            name: s.name,
            icon: "pin"
        }))
    ];

    let pathD = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
        const prev = points[i-1];
        const curr = points[i];
        const midX = (prev.x + curr.x) / 2;
        pathD += ` C ${midX} ${prev.y}, ${midX} ${curr.y}, ${curr.x} ${curr.y}`;
    }

    svg.innerHTML = `
        <defs>
            <pattern id="mapGrid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(232, 201, 122, 0.05)" stroke-width="0.5"/>
            </pattern>
            <linearGradient id="routeGoldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#38BDF8" />
                <stop offset="30%" stop-color="#A855F7" />
                <stop offset="70%" stop-color="#E8C97A" />
                <stop offset="100%" stop-color="#3CA082" />
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#mapGrid)" />
        <path d="${pathD}" fill="none" stroke="url(#routeGoldGrad)" stroke-width="3" stroke-dasharray="6,4" />

        ${points.map(p => `
            <g transform="translate(${p.x}, ${p.y})" style="cursor:pointer;">
                <circle r="12" fill="rgba(232, 201, 122, 0.2)" />
                <circle r="7" fill="${p.icon === 'plane' ? '#38BDF8' : (p.icon === 'hotel' ? '#A855F7' : '#E8C97A')}" stroke="#07090E" stroke-width="2" />
                <text y="-14" text-anchor="middle" fill="#CBD5E1" font-size="9" font-weight="700" font-family="'Plus Jakarta Sans', sans-serif">${p.name.substring(0, 14)}</text>
            </g>
        `).join('')}
    `;

    document.getElementById('mapInfoBadge').innerHTML = `<i class="fa-solid fa-route"></i> Route Mapped: ${org} Airport ➔ ${ap ? ap.primaryCode : 'Arrival'} ➔ Villa ➔ ${stops.length} Waypoints`;
}

function openCurrentDayGoogleMap() {
    const trip = store.getTrip(store.activeGuideTripId);
    const day = trip.days[store.activeGuideDayIndex];
    if (day && day.stops.length > 0) {
        const query = encodeURIComponent(`${day.stops[0].name}, ${trip.name}`);
        window.open(`https://maps.google.com/?q=${query}`, '_blank');
    }
}

// AUDIO SYNTHESIZER
function playAudioStory(tripId, dayIndex, stopId) {
    const trip = store.getTrip(tripId);
    const day = trip.days[dayIndex];
    const stop = day.stops.find(s => s.id === stopId);
    if (!stop || !stop.audioStory) return;

    store.activeAudioStory = stop.audioStory;
    
    document.getElementById('audioPlayerBar').style.display = 'flex';
    document.getElementById('barStoryTitle').textContent = stop.audioStory.title;
    document.getElementById('barStoryNarrator').textContent = `✦ Narrated for ${stop.name}`;

    document.getElementById('scriptModalTitle').textContent = stop.audioStory.title;
    document.getElementById('scriptModalText').textContent = `"${stop.audioStory.scriptText}"`;

    startAudioNarration();
}

function startAudioNarration() {
    if (!('speechSynthesis' in window)) {
        showToast("Audio synthesis not supported in this browser.");
        return;
    }

    window.speechSynthesis.cancel();
    const story = store.activeAudioStory;
    if (!story) return;

    const utterance = new SpeechSynthesisUtterance(story.scriptText);
    utterance.rate = store.speechRate;
    utterance.pitch = 1.0;

    const voices = window.speechSynthesis.getVoices();
    const premiumVoice = voices.find(v => (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.lang === 'en-US'));
    if (premiumVoice) utterance.voice = premiumVoice;

    utterance.onstart = () => { store.isPlayingAudio = true; updateAudioUi(true); };
    utterance.onend = () => { store.isPlayingAudio = false; updateAudioUi(false); };
    utterance.onerror = () => { store.isPlayingAudio = false; updateAudioUi(false); };

    store.speechUtterance = utterance;
    window.speechSynthesis.speak(utterance);
    showToast(`🎧 Playing audio: ${story.title}`);
}

function toggleAudioNarration() {
    if (store.isPlayingAudio) {
        window.speechSynthesis.pause();
        store.isPlayingAudio = false;
        updateAudioUi(false);
    } else {
        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
            store.isPlayingAudio = true;
            updateAudioUi(true);
        } else {
            startAudioNarration();
        }
    }
}

function stopAudioNarration() {
    window.speechSynthesis.cancel();
    store.isPlayingAudio = false;
    document.getElementById('audioPlayerBar').style.display = 'none';
    updateAudioUi(false);
}

function updateAudioUi(isPlaying) {
    const wave = document.getElementById('audioWaveAnim');
    const barPlayIcon = document.getElementById('barPlayIcon');
    const modalPlayIcon = document.getElementById('modalPlayBtnIcon');

    if (isPlaying) {
        wave.classList.remove('paused');
        if (barPlayIcon) barPlayIcon.className = 'fa-solid fa-pause';
        if (modalPlayIcon) modalPlayIcon.className = 'fa-solid fa-pause';
    } else {
        wave.classList.add('paused');
        if (barPlayIcon) barPlayIcon.className = 'fa-solid fa-play';
        if (modalPlayIcon) modalPlayIcon.className = 'fa-solid fa-play';
    }
}

function setSpeechRate(rate, btn) {
    store.speechRate = rate;
    document.querySelectorAll('#audioScriptModal .filter-chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    if (store.isPlayingAudio) startAudioNarration();
}

function openAudioStoryDetailModal() {
    if (!store.activeAudioStory) return;
    openModal('audioScriptModal');
}

// CREATOR HUB
function renderCreatorHub() {
    const videoContainer = document.getElementById('videoProofsContainer');
    videoContainer.innerHTML = store.data.videoProofs.map(v => `
        <div class="video-proof-card">
            <div class="video-thumb-wrap" onclick="openVideoProofModal('${v.id}')">
                <img src="${v.thumbnailUrl}" class="video-thumb-img" alt="${v.title}">
                <div class="video-play-overlay">
                    <div class="youtube-play-icon"><i class="fa-solid fa-play"></i></div>
                </div>
            </div>
            <div style="padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span class="gold-badge" style="font-size:10px;">${v.destination}</span>
                    <span style="font-size:11px; color:var(--text-muted);">${v.duration} · ${v.views}</span>
                </div>
                <h4 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">${v.title}</h4>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">
                    ${v.highlights.map(h => `<span class="tag-pill">✓ ${h}</span>`).join('')}
                </div>
            </div>
        </div>
    `).join('');

    renderReelsGrid();

    const reviewsContainer = document.getElementById('reviewsContainer');
    reviewsContainer.innerHTML = store.data.reviews.map(r => `
        <div class="review-card">
            <div class="review-header">
                <div>
                    <span style="font-size:13px; font-weight:800; color:#fff;">${r.authorHandle}</span>
                    <span style="font-size:10px; color:var(--text-muted); margin-left:6px;">· ${r.city}</span>
                </div>
                <div class="review-stars">
                    ${'<i class="fa-solid fa-star"></i>'.repeat(r.rating)}
                </div>
            </div>
            <span class="gold-badge" style="font-size:9px; margin-bottom:8px;">${r.tripTag}</span>
            <p class="review-quote">"${r.reviewQuote}"</p>
        </div>
    `).join('');
}

function renderReelsGrid() {
    const reelsContainer = document.getElementById('reelsGridContainer');
    const filtered = store.selectedReelsChannel === 'ALL'
        ? store.data.instagramPosts
        : store.data.instagramPosts.filter(p => p.channelType === store.selectedReelsChannel);

    reelsContainer.innerHTML = filtered.map(p => `
        <div class="reel-card" onclick="openInstagramChannel('${p.handle}')">
            <img src="${p.imageUrl}" class="reel-card-img" alt="${p.location}">
            <div class="reel-card-overlay">
                <span class="gold-badge" style="font-size:9px; align-self:flex-start;">${p.handle}</span>
                <div>
                    <div style="font-size:10px; color:var(--gold-light); font-weight:700;">📍 ${p.location}</div>
                    <div style="font-size:9px; color:var(--text-secondary); line-height:1.2; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">${p.caption}</div>
                    <div style="font-size:9px; color:#FFA090; margin-top:4px;"><i class="fa-solid fa-heart"></i> ${p.likesCount}</div>
                </div>
            </div>
        </div>
    `).join('');
}

function filterReelsChannel(channel, btn) {
    store.selectedReelsChannel = channel;
    document.querySelectorAll('#screen-hub .filter-chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderReelsGrid();
}

function openVideoProofModal(videoId) {
    const video = store.data.videoProofs.find(v => v.id === videoId);
    if (!video) return;

    document.getElementById('videoModalTitle').textContent = video.title;
    document.getElementById('videoModalIframe').src = video.videoUrl;
    document.getElementById('videoModalDetails').innerHTML = `
        <div style="font-size:13px; font-weight:800; color:var(--gold-light); margin-bottom:6px;">📍 ${video.destination} · ${video.views}</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;">
            ${video.highlights.map(h => `<span class="tag-pill">✓ ${h}</span>`).join('')}
        </div>
    `;

    openModal('videoProofModal');
}

// CUSTOM PLANNER
function sendCustomPlannerWhatsApp() {
    const org = store.selectedOrigin;
    const orgData = store.data.origins[org] || store.data.origins['BLR'];
    const dest = document.getElementById('planDestSelect').value;
    const vibe = document.querySelector('input[name="planVibe"]:checked').value;
    const squad = document.getElementById('planSquadSelect').value;
    const date = document.getElementById('planDateInput').value || 'Flexible / Upcoming Friday';
    const budget = document.getElementById('planBudgetInput').value || 'Standard Verified Tier';
    const notes = document.getElementById('planNotesInput').value || 'None';

    const msg = `✦ *NEW AIRPORT TRIP INQUIRY — ComeTripWithMe* ✦\n\n` +
                `🛫 *Departing From:* ${orgData.name} (${orgData.code} - ${orgData.airport})\n` +
                `📍 *Destination:* ${dest}\n` +
                `✨ *Vibe:* ${vibe}\n` +
                `👥 *Squad Size:* ${squad}\n` +
                `🗓️ *Dates:* ${date}\n` +
                `💰 *Budget Target:* ${budget}\n` +
                `📝 *Transit & Stay Requests:* ${notes}\n\n` +
                `Please send available flight slots and the verified creator itinerary!`;

    openWhatsAppLink(msg);
}

function sendCustomPlannerEmail() {
    const org = store.selectedOrigin;
    const dest = document.getElementById('planDestSelect').value;
    const squad = document.getElementById('planSquadSelect').value;
    const subject = encodeURIComponent(`Airport Booking: ${org} to ${dest} for ${squad}`);
    const body = encodeURIComponent(`Hi ComeTripWithMe team,\n\nI want to plan a custom trip from ${org} to ${dest}.\nPlease share available flights, airport cab pickup and resort details.\n\nThank you!`);
    window.location.href = `mailto:${store.data.branding.email}?subject=${subject}&body=${body}`;
}

// SAVED TRIPS & PACKING
function renderWishlist() {
    const count = store.data.wishlist.length;
    document.getElementById('wishlistCount').textContent = count;

    const container = document.getElementById('wishlistContainer');
    if (count === 0) {
        container.innerHTML = `
            <div class="glass-panel" style="text-align:center; padding:24px;">
                <i class="fa-regular fa-heart" style="font-size:32px; color:var(--text-tertiary); margin-bottom:8px;"></i>
                <h4 style="font-size:14px; font-weight:800; color:#fff;">No Wishlisted Trips Yet</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-top:4px;">Tap the heart icon on any trip in the Explore tab to save it here.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = store.data.wishlist.map(tripId => {
        const trip = store.getTrip(tripId);
        return `
            <div class="trip-card" style="margin-bottom:12px;" onclick="openTripDetailModal('${trip.id}')">
                <div style="display:flex; align-items:center; gap:12px; padding:12px;">
                    <img src="${trip.imageUrl}" style="width:70px; height:70px; border-radius:var(--radius-md); object-fit:cover;" alt="${trip.name}">
                    <div style="flex:1;">
                        <h4 style="font-size:14px; font-weight:800; color:#fff;">${trip.name}</h4>
                        <div style="font-size:11px; color:var(--gold-primary); font-weight:700;">${trip.price} · ${trip.duration}</div>
                        <span class="vibe-badge vibe-${trip.vibe.toLowerCase()}" style="font-size:9px; margin-top:4px;">${getVibeEmoji(trip.vibe)} ${trip.vibe}</span>
                    </div>
                    <button class="icon-circle-btn" onclick="event.stopPropagation(); store.toggleWishlist('${trip.id}');" title="Remove">
                        <i class="fa-solid fa-trash" style="font-size:12px; color:#FFA090;"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function renderPackingList(categoryFilter = 'ALL') {
    const container = document.getElementById('packingListContainer');
    const items = categoryFilter === 'ALL'
        ? store.data.packingItems
        : store.data.packingItems.filter(i => i.category === categoryFilter);

    const total = store.data.packingItems.length;
    const checked = store.data.packingItems.filter(i => i.isChecked).length;
    const pct = total > 0 ? Math.round((checked / total) * 100) : 0;
    document.getElementById('packingProgressText').textContent = `${checked} / ${total} items packed (${pct}%)`;

    container.innerHTML = items.map(item => `
        <div class="packing-item-row ${item.isChecked ? 'checked' : ''}" onclick="togglePackingItem('${item.id}')">
            <div style="display:flex; align-items:center; gap:10px;">
                <div class="custom-checkbox">
                    <i class="fa-solid fa-check"></i>
                </div>
                <div>
                    <div style="font-size:12px; font-weight:700; color:#fff;">${item.title}</div>
                    <span style="font-size:9px; color:var(--gold-primary);">${item.category}</span>
                </div>
            </div>
            <button class="icon-circle-btn" style="width:28px; height:28px; border:none; background:transparent;" onclick="event.stopPropagation(); deletePackingItem('${item.id}')">
                <i class="fa-solid fa-xmark" style="font-size:12px; color:var(--text-tertiary);"></i>
            </button>
        </div>
    `).join('');
}

function filterPackingCategory(cat, btn) {
    document.querySelectorAll('#screen-saved .filter-chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderPackingList(cat);
}

function togglePackingItem(itemId) {
    const item = store.data.packingItems.find(i => i.id === itemId);
    if (item) {
        item.isChecked = !item.isChecked;
        store.save();
        renderPackingList();
    }
}

function deletePackingItem(itemId) {
    store.data.packingItems = store.data.packingItems.filter(i => i.id !== itemId);
    store.save();
    renderPackingList();
    showToast("Item removed from packing checklist");
}

function promptAddPackingItem() {
    const title = prompt("Enter packing item name:");
    if (title && title.trim()) {
        const category = prompt("Category (Essentials, Tech, Apparel, Care, Personal):", "Personal") || "Personal";
        store.data.packingItems.push({
            id: 'p_' + Date.now(),
            title: title.trim(),
            category: category.trim(),
            isChecked: false
        });
        store.save();
        renderPackingList();
        showToast("Added to packing checklist ✦");
    }
}

// MASTER CMS & CONTROLLER
function switchCmsTab(tabId, btn) {
    document.querySelectorAll('.cms-tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    document.getElementById('cms-section-brand').style.display = tabId === 'brand' ? 'block' : 'none';
    document.getElementById('cms-section-transit').style.display = tabId === 'transit' ? 'block' : 'none';
    document.getElementById('cms-section-trips').style.display = tabId === 'trips' ? 'block' : 'none';
    document.getElementById('cms-section-audio').style.display = tabId === 'audio' ? 'block' : 'none';
    document.getElementById('cms-section-data').style.display = tabId === 'data' ? 'block' : 'none';

    if (tabId === 'transit') renderCmsTransitEditor();
    if (tabId === 'trips') renderCmsTripsList();
    if (tabId === 'audio') renderCmsAudioList();
}

function populateCmsFields() {
    const b = store.data.branding;
    document.getElementById('cmsBrandTitle').value = b.title;
    document.getElementById('cmsBrandSubtitle').value = b.subtitle;
    document.getElementById('cmsWhatsAppNum').value = b.whatsapp;
    document.getElementById('cmsPhoneNum').value = b.phone;
    document.getElementById('cmsEmail').value = b.email;
    document.getElementById('cmsHandleTravel').value = b.instagramTravel;
    document.getElementById('cmsHandleFood').value = b.instagramFood;
}

function saveCmsBranding() {
    const b = store.data.branding;
    b.title = document.getElementById('cmsBrandTitle').value.trim();
    b.subtitle = document.getElementById('cmsBrandSubtitle').value.trim();
    b.whatsapp = document.getElementById('cmsWhatsAppNum').value.trim();
    b.phone = document.getElementById('cmsPhoneNum').value.trim();
    b.email = document.getElementById('cmsEmail').value.trim();
    b.instagramTravel = document.getElementById('cmsHandleTravel').value.trim();
    b.instagramFood = document.getElementById('cmsHandleFood').value.trim();

    store.save();
    applyBrandingUi();
    showToast("Branding & contacts updated live! ✦");
}

function applyBrandingUi() {
    const b = store.data.branding;
    document.getElementById('appBrandTitle').textContent = b.title;
    document.getElementById('appBrandSubtitle').textContent = b.subtitle;
    document.getElementById('footerBrandName').textContent = b.title;
}

function renderCmsTransitEditor() {
    const container = document.getElementById('cmsTransitEditorContainer');
    container.innerHTML = store.data.trips.map(t => {
        const ap = t.airportInfo;
        const routes = t.originRoutes || {};
        return `
            <div class="glass-panel" style="padding:14px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <h4 style="font-size:14px; font-weight:800; color:#fff;">${t.name} (${ap ? ap.primaryCode : 'AIRPORT'})</h4>
                        <span style="font-size:10px; color:var(--gold-primary);">${ap ? ap.primaryName : ''}</span>
                    </div>
                    <button class="gold-badge" onclick="promptEditAirport('${t.id}')">
                        <i class="fa-solid fa-pen"></i> Edit
                    </button>
                </div>
                <div style="font-size:11px; color:var(--text-secondary); line-height:1.4;">
                    🛫 <strong>BLR Route:</strong> ${routes['BLR'] ? routes['BLR'].transport : 'N/A'} (Dep: ${routes['BLR'] ? routes['BLR'].departureTime : 'N/A'})<br>
                    🛫 <strong>DEL Route:</strong> ${routes['DEL'] ? routes['DEL'].transport : 'N/A'} (Dep: ${routes['DEL'] ? routes['DEL'].departureTime : 'N/A'})<br>
                    🛫 <strong>BOM Route:</strong> ${routes['BOM'] ? routes['BOM'].transport : 'N/A'} (Dep: ${routes['BOM'] ? routes['BOM'].departureTime : 'N/A'})
                </div>
            </div>
        `;
    }).join('');
}

function promptEditAirport(tripId) {
    const t = store.getTrip(tripId);
    if (!t.airportInfo) return;
    const newCode = prompt("Destination Primary Airport Code (e.g. GOX, BKK):", t.airportInfo.primaryCode);
    if (newCode) t.airportInfo.primaryCode = newCode.toUpperCase();
    store.save();
    renderExploreTrips();
    renderCmsTransitEditor();
    showToast(`Updated airport code for ${t.name} ✦`);
}

function renderCmsTripsList() {
    const container = document.getElementById('cmsTripsListContainer');
    container.innerHTML = store.data.trips.map(t => `
        <div class="glass-panel" style="padding:12px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <h4 style="font-size:13px; font-weight:800; color:#fff;">${t.name} (${t.duration})</h4>
                <span class="gold-badge" style="font-size:10px;">${t.price}</span>
            </div>
            <p style="font-size:11px; color:var(--text-muted); margin-bottom:8px;">${t.headline}</p>
            <div style="display:flex; gap:6px; justify-content:flex-end;">
                <button class="gold-btn" style="padding:4px 10px; font-size:10px;" onclick="editTripPrompt('${t.id}')">
                    <i class="fa-solid fa-pen"></i> Edit
                </button>
                <button class="glass-btn" style="padding:4px 10px; font-size:10px; color:#FFA090;" onclick="deleteTripCms('${t.id}')">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function editTripPrompt(tripId) {
    const t = store.getTrip(tripId);
    const newName = prompt("Trip Name:", t.name);
    if (!newName) return;
    const newPrice = prompt("Price:", t.price);
    if (!newPrice) return;
    const newHeadline = prompt("Headline:", t.headline);

    t.name = newName;
    t.price = newPrice;
    if (newHeadline) t.headline = newHeadline;

    store.save();
    renderExploreTrips();
    renderCmsTripsList();
    showToast(`Updated ${t.name} ✦`);
}

function deleteTripCms(tripId) {
    if (confirm("Delete this trip?")) {
        store.data.trips = store.data.trips.filter(t => t.id !== tripId);
        store.save();
        renderExploreTrips();
        renderCmsTripsList();
        showToast("Trip deleted.");
    }
}

function promptAddNewTrip() {
    const name = prompt("New Destination Name (e.g. Coorg):");
    if (!name) return;
    const airport = prompt("Nearest Airport Code (e.g. MYQ / BLR):", "BLR") || "BLR";
    const price = prompt("Price Estimate (e.g. ₹5,999):", "₹5,999");
    const id = name.toLowerCase().replace(/[^a-z0-9]/g, '_');

    const newTrip = {
        id: id,
        name: name,
        headline: "Handcrafted creator route, coffee estates & misty peaks.",
        description: `Verified 3-day itinerary exploring the hidden gems and secret trails of ${name}.`,
        vibe: "CHILL",
        duration: "3D · 2N",
        price: price || "₹5,999",
        budgetValue: 5999,
        imageUrl: "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?w=800&q=80",
        heroTags: [`${airport} Gateway`, name, "Creator Verified"],
        totalEstimateDetails: "Covers 2 nights boutique plantation stay & local food crawl.",
        creatorNote: "Scouted and verified by ComeTripWithMe.",
        airportInfo: {
            primaryCode: airport.toUpperCase(),
            primaryName: `${name} Airport Gateway`,
            arrivalTerminal: "Main Terminal",
            baggageCarousel: "Belt 1"
        },
        originRoutes: {
            "BLR": { originCode: "BLR", originName: "Bengaluru", transport: "Direct AC Highway Cab / Flight", terminal: "BLR Gateway", gate: "Bay 1", boardingTime: "06:00 AM", departureTime: "06:30 AM", arrivalTime: "11:00 AM", duration: "4h 30m scenic drive", pnr: `CTWM-BLR-${airport}` },
            "DEL": { originCode: "DEL", originName: "Delhi", transport: "Flight to BLR/MYQ + Scenic Cab", terminal: "DEL T3", gate: "Gate 14", boardingTime: "06:00 AM", departureTime: "06:45 AM", arrivalTime: "12:30 PM", duration: "5h 45m total", pnr: `CTWM-DEL-${airport}` },
            "BOM": { originCode: "BOM", originName: "Mumbai", transport: "Flight to BLR/MYQ + Scenic Cab", terminal: "BOM T2", gate: "Gate 22", boardingTime: "06:30 AM", departureTime: "07:15 AM", arrivalTime: "01:00 PM", duration: "5h 45m total", pnr: `CTWM-BOM-${airport}` }
        },
        cabTransfer: {
            pickupLocation: "Airport Exit Bay 1",
            vehicle: "Toyota Innova (KA-12-Z-9912)",
            driverName: "Kariappa",
            driverPhone: "+919742311023",
            durationToHotel: "25 mins plantation road drive"
        },
        hotelStay: {
            name: `${name} Misty Plantation Estate Villa`,
            address: `Coffee Estate Road, ${name}, Karnataka`,
            mapLink: `https://maps.google.com/?q=${name}`,
            checkInTime: "12:30 PM",
            checkOutTime: "11:00 AM",
            roomType: "Coffee Trail Suite with Mist Balcony",
            wifiSsid: `${name}_Estate_Guest`,
            wifiPass: "estatecoffee2025",
            hostName: "Appanna (Host)",
            hostPhone: "+919742311023"
        },
        days: [
            {
                dayNumber: 1,
                title: `${name} Scenic Discovery`,
                summary: `Morning plantation crawl, scenic viewpoint, and local cuisine.`,
                creatorSecretTip: "Start early to avoid tourist traffic.",
                stops: [
                    {
                        id: `${id}_d1_s1`,
                        name: `${name} Viewpoint Point`,
                        timing: "08:00 AM",
                        interStopTransit: "🚖 20 mins private jeep drive to peak",
                        category: "Scenic Lookout",
                        description: `Panoramic vistas over the valleys of ${name}.`,
                        insiderTip: "Bring binoculars for bird watching.",
                        photoUrl: "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?w=600&q=80",
                        lat: 12.4,
                        lng: 75.7
                    }
                ],
                foodSpots: []
            }
        ]
    };

    store.data.trips.unshift(newTrip);
    store.save();
    renderExploreTrips();
    renderCmsTripsList();
    showToast(`✦ Added new trip: ${name} (${airport})!`);
}

function renderCmsAudioList() {
    const container = document.getElementById('cmsAudioStoriesList');
    let stories = [];
    store.data.trips.forEach(t => {
        t.days.forEach(d => {
            d.stops.forEach(s => {
                if (s.audioStory) {
                    stories.push({ trip: t.name, stop: s.name, story: s.audioStory });
                }
            });
        });
    });

    container.innerHTML = stories.map(st => `
        <div class="glass-panel" style="padding:12px; margin-bottom:10px;">
            <div style="font-size:12px; font-weight:800; color:var(--gold-light);">${st.story.title}</div>
            <div style="font-size:10px; color:var(--text-muted); margin-bottom:6px;">📍 ${st.stop} (${st.trip})</div>
            <p style="font-size:11px; color:var(--text-secondary); line-height:1.4; font-style:italic;">"${st.story.scriptText}"</p>
        </div>
    `).join('');
}

function exportAppDataJson() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(store.data, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", "cometripwithme_airport_app_database.json");
    dlAnchor.click();
    showToast("Database exported as JSON ✦");
}

function importAppDataJson(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const imported = JSON.parse(e.target.result);
            if (imported.trips && imported.branding) {
                store.data = imported;
                store.save();
                applyBrandingUi();
                renderExploreScreen();
                renderCreatorHub();
                renderWishlist();
                renderPackingList();
                showToast("✦ Database imported and applied successfully!");
            } else {
                alert("Invalid ComeTripWithMe JSON database structure.");
            }
        } catch(err) {
            alert("Error parsing JSON file: " + err.message);
        }
    };
    reader.readAsText(file);
}

function resetToFactoryCuratedData() {
    if (confirm("Reset everything back to factory default ComeTripWithMe data?")) {
        store.data = JSON.parse(JSON.stringify(FACTORY_DATA));
        store.save();
        applyBrandingUi();
        renderExploreScreen();
        renderCreatorHub();
        renderWishlist();
        renderPackingList();
        showToast("Database restored to default factory state ✦");
    }
}

// External Launchers
function openWhatsAppInquiry() {
    const org = store.selectedOrigin;
    openWhatsAppLink(`Hey ComeTripWithMe! ✦ I'd like to plan an airport route departing from ${org}.`);
}

function inquireTripWhatsApp(tripId) {
    const trip = store.getTrip(tripId);
    const org = store.selectedOrigin;
    const route = store.getOriginRoute(trip);
    const msg = `Hey ComeTripWithMe! ✦ I'm interested in booking the *${trip.name}* trip (${trip.price}) departing from *${org}* (${route ? route.transport : 'Flight'}). Can you share available departure slots?`;
    openWhatsAppLink(msg);
}

function openWhatsAppLink(msg) {
    const num = store.data.branding.whatsapp || "919742311023";
    const url = `https://wa.me/${num}?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
}

function openInstagramChannel(handle = "@cometriipwme") {
    const clean = handle.replace('@', '');
    window.open(`https://instagram.com/${clean}`, '_blank');
}

function openYouTubeChannel() {
    window.open(`https://youtube.com/@${store.data.branding.youtube}`, '_blank');
}

// Modals & Helpers
function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add('open');
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('open');
        if (id === 'videoProofModal') {
            document.getElementById('videoModalIframe').src = '';
        }
    }
}

function showToast(text) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast-msg';
    toast.innerHTML = `<i class="fa-solid fa-plane-departure" style="color:var(--gold-primary);"></i> ${text}`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

function updateClock() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const clockEl = document.getElementById('liveClock');
    if (clockEl) clockEl.textContent = `${hours % 12 || 12}:${minutes}`;
}

window.addEventListener('DOMContentLoaded', () => {
    updateClock();
    setInterval(updateClock, 30000);

    applyBrandingUi();
    renderExploreScreen();
    renderCreatorHub();
    renderWishlist();
    renderPackingList();

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-backdrop.open').forEach(m => m.classList.remove('open'));
            const drawer = document.getElementById('cmsDrawer');
            if (drawer.classList.contains('open')) toggleCmsDrawer();
        }
    });

    console.log("✨ ComeTripWithMe Airport & Multi-City Hub Engine loaded.");
});
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated index.html successfully with {len(html_content)} characters.")
