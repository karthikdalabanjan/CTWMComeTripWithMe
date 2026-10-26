import json

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ComeTripWithMe · Creator Tour Operator (Luxury · Mid-Tier · Budget)</title>
    <meta name="description" content="Creator-led curated travel itineraries across Luxury, Mid-Tier, and Budget segments. Direct flights, Volvo sleeper buses, express trains, 5-star resorts, boutique hotels, and social hostels.">
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
            --accent-orange: #FB923C;
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

        /* Tier Segment Badges & Pills */
        .tier-pill-selector {
            display: flex;
            background: rgba(7, 9, 14, 0.8);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-full);
            padding: 3px;
            gap: 4px;
            margin: 10px 0 12px;
        }
        .tier-pill-btn {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-family: var(--font-heading);
            font-size: 10px;
            font-weight: 700;
            padding: 6px 8px;
            border-radius: var(--radius-full);
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }
        .tier-pill-btn:hover {
            color: #fff;
        }
        .tier-pill-btn.active-tier-budget {
            background: rgba(56, 189, 248, 0.25);
            color: #7DD3FC;
            border: 1px solid rgba(56, 189, 248, 0.5);
            box-shadow: 0 2px 8px rgba(56, 189, 248, 0.3);
        }
        .tier-pill-btn.active-tier-mid {
            background: rgba(232, 201, 122, 0.25);
            color: var(--gold-light);
            border: 1px solid var(--gold-primary);
            box-shadow: 0 2px 8px rgba(232, 201, 122, 0.3);
        }
        .tier-pill-btn.active-tier-luxury {
            background: linear-gradient(135deg, var(--gold-primary), var(--gold-secondary));
            color: var(--bg-dark);
            font-weight: 900;
            box-shadow: 0 2px 10px rgba(232, 201, 122, 0.5);
        }

        .tier-badge {
            font-size: 10px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: var(--radius-full);
            display: inline-flex;
            align-items: center;
            gap: 4px;
            letter-spacing: 0.3px;
        }
        .tier-badge.budget {
            background: rgba(56, 189, 248, 0.18);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #7DD3FC;
        }
        .tier-badge.mid {
            background: rgba(232, 201, 122, 0.18);
            border: 1px solid var(--glass-border-strong);
            color: var(--gold-light);
        }
        .tier-badge.luxury {
            background: linear-gradient(135deg, var(--gold-primary), var(--gold-secondary));
            color: var(--bg-dark);
            font-weight: 900;
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
            background: rgba(7, 9, 14, 0.92);
            border: 1px solid var(--glass-border-strong);
            padding: 4px 12px;
            border-radius: var(--radius-full);
            font-family: var(--font-heading);
            font-size: 14px;
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

                <!-- ================= TAB 1: EXPLORE (3-TIER SEGMENTS) ================= -->
                <section class="screen-view active-screen" id="screen-explore">
                    
                    <!-- Hero Banner -->
                    <div class="hero-banner-card">
                        <div class="hero-banner-content">
                            <span class="gold-badge" id="heroOriginTag">✦ LUXURY · MID-TIER · BUDGET SEGMENTS · MULTI-CITY</span>
                            <h1 class="hero-title">Creator Travel Across Luxury, Mid-Tier & Budget Segments</h1>
                            <p class="hero-desc">Choose between 5-Star Resorts + Innova Cabs (Luxury), Boutique Hotels + Flights (Mid-Tier), or Social Hostels + Sleeper Coaches (Budget).</p>
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

                    <!-- Travel Segment Switcher Filter (All, Budget, Mid, Luxury) -->
                    <div class="section-title-wrap">
                        <div>
                            <h2 class="section-title"><span class="sparkle">✦</span> Travel Segments</h2>
                            <p class="section-subtitle">Tailored transport & accommodation classes</p>
                        </div>
                    </div>
                    <div class="scroll-chips-row" id="segmentFilterChips">
                        <button class="filter-chip active" onclick="filterTripsBySegment('ALL', this)">All Segments</button>
                        <button class="filter-chip" onclick="filterTripsBySegment('budget', this)">🎒 Budget (Hostel + Bus/Train)</button>
                        <button class="filter-chip" onclick="filterTripsBySegment('mid', this)">✨ Mid-Tier (Boutique Hotel + Flight/Cab)</button>
                        <button class="filter-chip" onclick="filterTripsBySegment('luxury', this)">🌟 Luxury (5-Star Resort + Innova Cab)</button>
                    </div>

                    <!-- Destination Spotlights by Airport Gateway -->
                    <div class="section-title-wrap">
                        <div>
                            <h2 class="section-title"><span class="sparkle">✦</span> Airport Gateways & Spotlights</h2>
                            <p class="section-subtitle">Direct connections from <span id="spotlightOriginName" style="color:var(--gold-light); font-weight:700;">Bengaluru (BLR)</span></p>
                        </div>
                    </div>
                    <div class="spotlights-carousel" id="spotlightsContainer"></div>

                    <!-- Trips Grid -->
                    <div class="section-title-wrap">
                        <div>
                            <h2 class="section-title"><span class="sparkle">✦</span> Curated Creator Itineraries</h2>
                            <p class="section-subtitle">Toggle tiers on each card to compare price, stays & transit</p>
                        </div>
                    </div>
                    <div class="trips-grid" id="tripsGridContainer"></div>

                    <!-- Smart Match Trip Recommender Box -->
                    <div class="smart-match-box">
                        <div class="section-title-wrap" style="margin-bottom:6px;">
                            <div>
                                <span class="gold-badge" style="margin-bottom:6px;">✦ AI SMART MATCH</span>
                                <h3 class="section-title">Instant Flight & Tier Matcher</h3>
                            </div>
                        </div>
                        <p style="font-size:12px; color:var(--text-secondary); margin-bottom:14px;">Find the exact itinerary matched to your departure origin, preferred segment, and squad.</p>

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
                                <label class="match-field-label">Preferred Travel Segment</label>
                                <select class="match-input-select" id="smartTierSelect" onchange="runSmartMatch()">
                                    <option value="mid">✨ Mid-Tier (Boutique Hotel + Flight/Cab)</option>
                                    <option value="budget">🎒 Budget (Hostel + Bus/Train)</option>
                                    <option value="luxury">🌟 Luxury (5-Star Resort + Innova)</option>
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
                                    View Recommended Itinerary ✦
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
                        <p style="font-size:12px; color:var(--text-secondary); line-height:1.5;">India's first creator-led tour operator. Verified routes across Luxury, Mid-Tier and Budget classes. Based in Bengaluru, Delhi & Mumbai ☕.</p>
                        
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
                                <span>T-3h Departure</span>
                                <span>🚖 Cab Pickup</span>
                                <span>🏨 Stay Arrival</span>
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
                            <p class="section-subtitle">Live GPS transit corridor & accommodation pins</p>
                        </div>
                        <button class="gold-badge" style="cursor:pointer;" onclick="openCurrentDayGoogleMap()">
                            <i class="fa-solid fa-map-location-dot"></i> Maps
                        </button>
                    </div>
                    <div class="route-map-box">
                        <svg class="map-svg-canvas" id="routeMapSvg" viewBox="0 0 400 200"></svg>
                        <div class="map-info-badge" id="mapInfoBadge">
                            <i class="fa-solid fa-route"></i> Route Mapped: Departure Hub ➔ Stay ➔ Waypoints
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
                            <p class="section-subtitle">Real feedback across Luxury, Mid-Tier & Budget travelers</p>
                        </div>
                    </div>
                    <div id="reviewsContainer"></div>
                </section>

                <!-- ================= TAB 4: TRIP PLANNER (WITH TIER SELECTION) ================= -->
                <section class="screen-view" id="screen-planner">
                    <div class="section-title-wrap">
                        <div>
                            <span class="gold-badge" style="margin-bottom:6px;">✦ CUSTOM CREATOR ITINERARY</span>
                            <h2 class="section-title">Trip Planner & Builder</h2>
                            <p class="section-subtitle">Choose departure city, travel segment & get a custom itinerary on WhatsApp</p>
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

                    <!-- Step 2: Travel Segment -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">2</span>
                            <h3 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">Select Travel Segment Class</h3>
                        </div>
                        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
                            <label class="filter-chip" style="display:flex; align-items:center; gap:4px; font-size:11px; cursor:pointer;">
                                <input type="radio" name="plannerTier" value="🎒 Budget (Hostel + Bus/Train)"> 🎒 Budget
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:4px; font-size:11px; cursor:pointer;">
                                <input type="radio" name="plannerTier" value="✨ Mid-Tier (Boutique + Flight/Cab)" checked> ✨ Mid-Tier
                            </label>
                            <label class="filter-chip" style="display:flex; align-items:center; gap:4px; font-size:11px; cursor:pointer;">
                                <input type="radio" name="plannerTier" value="🌟 Luxury (5-Star + Innova)"> 🌟 Luxury
                            </label>
                        </div>
                    </div>

                    <!-- Step 3: Destination -->
                    <div class="planner-step-card">
                        <div style="display:flex; align-items:center; margin-bottom:12px;">
                            <span class="planner-step-number">3</span>
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
                            <input type="text" class="match-input-text" id="planBudgetInput" placeholder="e.g. ₹5,000 - ₹20,000">
                        </div>
                        <div>
                            <label class="match-field-label">Special Requests / Stay Preferences</label>
                            <textarea class="match-input-text" id="planNotesInput" rows="3" placeholder="e.g. Need private pool villa, pure veg breakfast, airport pickup, pet friendly..."></textarea>
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
                <span class="gold-badge" style="margin-bottom:4px;">✦ OFFICIAL BOOKING & TRANSIT PASS</span>
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
            <button class="cms-tab-btn" onclick="switchCmsTab('transit', this)">Tier Logistics & Stays</button>
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
                <label class="match-field-label">WhatsApp Contact Number</label>
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

        <!-- CMS Tab 2: Tier Logistics Manager -->
        <div id="cms-section-transit" style="display:none;">
            <p style="font-size:12px; color:var(--text-secondary); margin-bottom:12px;">Live edit Luxury, Mid-Tier, and Budget segment pricing, transport (flights, sleeper buses, trains, cabs) and accommodation.</p>
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
 * COMETRIPWITHME - MASTER DATA & REACTIVE LOGIC ENGINE WITH 3-TIER TRAVEL SEGMENTS (LUXURY / MID-TIER / BUDGET)
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
        bookingId: "CTWM-MID-GOA-8842",
        bookedTripId: "goa",
        departureOrigin: "BLR",
        selectedTier: "mid", // 'budget', 'mid', 'luxury'
        squadSize: "2 of us",
        travelDate: "Upcoming Friday",
        status: "CONFIRMED & TICKETED"
    },
    origins: {
        "BLR": { code: "BLR", name: "Bengaluru", airport: "Kempegowda Intl (BLR)", busStation: "Majestic / Satellite ISBT", trainStation: "KSR Bengaluru (SBC)" },
        "DEL": { code: "DEL", name: "Delhi", airport: "Indira Gandhi Intl (DEL)", busStation: "ISBT Kashmere Gate", trainStation: "New Delhi Railway (NDLS)" },
        "BOM": { code: "BOM", name: "Mumbai", airport: "Chhatrapati Shivaji Maharaj (BOM)", busStation: "Borivali / Dadar Private Terminal", trainStation: "CSMT / Bandra Terminus" }
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
            imageUrl: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80",
            heroTags: ["GOX Mopa Airport", "Cliff Views", "Kayaking", "Secret Bakeries"],
            creatorNote: "We scouted every single stop in December 2024 to make sure the vibe is completely untarnished.",
            
            airportInfo: {
                primaryCode: "GOX",
                primaryName: "Goa Manohar International Airport (Mopa)",
                alternateCode: "GOI",
                alternateName: "Dabolim International Airport (South Goa)"
            },

            // 3-Tier Segment Booking Matrix
            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹3,999",
                    budgetValue: 3999,
                    transportType: "🚌 AC Sleeper Bus / 🚆 Express Train",
                    transportDetails: "Multi-Axle AC Sleeper Bus / Vasco Express 3AC",
                    departureHub: "Majestic / Kashmere Gate / Borivali Private Stand",
                    arrivalStation: "Madgaon Junction / Panjim Central Bus Stand",
                    transferMode: "Shared Auto / Scooty Handover at Station",
                    stayName: "Zostel North Goa / Anjuna Beach Eco Shacks",
                    stayType: "Social Backpacker Hostel (AC 6-Bed Dorm / Beach Hut)",
                    stayAddress: "Anjuna Beach Rd, North Goa",
                    inclusions: ["AC Dorm Bed / Shack", "Self-Drive Scooty Rental with Helmet", "Hostel Community Pub Crawl", "Pocket Audio Guide Pass"],
                    pnrPrefix: "CTWM-BUS-GOA"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹8,999",
                    budgetValue: 8999,
                    transportType: "✈️ Direct Flight + 🚖 AC Sedan Cab",
                    transportDetails: "IndiGo / Akasa Air Direct Flight (BLR/DEL/BOM ➔ GOX)",
                    departureHub: "Airport T2 (BLR) / T3 (DEL) / T2 (BOM) Departure Gate",
                    arrivalStation: "Goa Manohar Mopa Airport (GOX) Terminal 1",
                    transferMode: "Pre-booked AC Dzire/Ertiga Airport Transfer",
                    stayName: "Casa Vagator Boutique Ocean Resort",
                    stayType: "3-4 Star Curated Boutique Resort (Private AC Room with Balcony)",
                    stayAddress: "Small Vagator Cliff Road, North Goa",
                    inclusions: ["Private Boutique Room", "Airport Cab Transfers", "Scooty with Fuel Allowance", "Cafe Breakfasts", "Pocket Audio Guide"],
                    pnrPrefix: "CTWM-MID-GOA"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹18,999",
                    budgetValue: 18999,
                    transportType: "✈️ Premium Flight + 🚖 Innova Crysta Chauffeur",
                    transportDetails: "Air India / Vistara Direct Flight + Dedicated Chauffeur",
                    departureHub: "Airport VIP Terminal Chauffeur Lane",
                    arrivalStation: "Goa Manohar Mopa (GOX) VIP Arrival Gate",
                    transferMode: "Dedicated Innova Crysta Luxury Chauffeur for all 4 Days",
                    stayName: "Thalassa Luxury Cliffside Villa & Resort",
                    stayType: "5-Star Oceanfront Private Pool Villa",
                    stayAddress: "Plot 14, Small Vagator Cliff Trail, North Goa",
                    inclusions: ["5-Star Private Pool Villa", "24/7 Innova Crysta Chauffeur", "VIP Sunset Table at Thalassa", "Fine Dining Dinner Passes", "Private Speedboat Tour"],
                    pnrPrefix: "CTWM-LUX-GOA"
                }
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
            imageUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
            heroTags: ["BKK Suvarnabhumi", "Krabi KBV", "Longtail Boats", "Night Markets"],
            creatorNote: "Bangkok street food is best at 11 PM in Chinatown. We mapped the exact 4 stalls that locals eat at.",
            
            airportInfo: {
                primaryCode: "BKK",
                primaryName: "Bangkok Suvarnabhumi International Airport",
                alternateCode: "DMK",
                alternateName: "Don Mueang International Airport"
            },

            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹14,999",
                    budgetValue: 14999,
                    transportType: "✈️ Economy Flight + 🚆 MRT/BTS & Ferry",
                    transportDetails: "AirAsia Economy + Airport Rail Link & Shared Krabi Express Ferry",
                    departureHub: "T2 International (BLR/BOM) / T3 (DEL)",
                    arrivalStation: "Bangkok BKK / Krabi Pier",
                    transferMode: "Bangkok Subway Card & Shared Longtail Transfer",
                    stayName: "Mad Monkey Bangkok Chinatown & Slumber Party Krabi",
                    stayType: "High-Rated Social Backpacker Hostel (AC Pod / Dorm)",
                    stayAddress: "Chinatown & Ao Nang Beach",
                    inclusions: ["Hostel Pod Bed", "4 Islands Shared Longtail Tour", "Chinatown Midnight Wok Crawl", "Hostel Pool Pass"],
                    pnrPrefix: "CTWM-BUD-THAI"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹24,999",
                    budgetValue: 24999,
                    transportType: "✈️ Direct Flight + 🚐 VIP Van & Longtail",
                    transportDetails: "Thai Airways / IndiGo Direct Flight + VIP Commuter Van",
                    departureHub: "T2 / T3 International Terminal",
                    arrivalStation: "Suvarnabhumi BKK Level 2 / Krabi KBV",
                    transferMode: "Private Airport Van & Traditional Longtail Boat",
                    stayName: "ASAI Bangkok Chinatown & Panan Krabi Boutique Resort",
                    stayType: "4-Star Curated Boutique Stays (Private King Room)",
                    stayAddress: "531 Charoen Krung Rd & Ao Nang Cliff",
                    inclusions: ["4-Star Boutique Rooms", "Private Traditional Longtail Tour", "Daily Buffet Breakfast", "Chinatown Food Pass"],
                    pnrPrefix: "CTWM-MID-THAI"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹48,999",
                    budgetValue: 48999,
                    transportType: "✈️ Premium Business Flight + 🛥️ Private Yacht",
                    transportDetails: "Thai Airways Royal Silk / Flex + Luxury Toyota Vellfire & Private Speedboat",
                    departureHub: "Airport VIP Business Class Lounge",
                    arrivalStation: "Suvarnabhumi VIP Fast-Track Gate",
                    transferMode: "Dedicated Toyota Vellfire Chauffeur & Private Speedboat Charter",
                    stayName: "The Standard Bangkok Mahanakhon & Rayavadee Luxury Resort",
                    stayType: "5-Star Luxury Skyline Suite & Beachfront Pavilion Villa",
                    stayAddress: "Mahanakhon Tower & Railay Beach, Krabi",
                    inclusions: ["5-Star Beachfront Pavilion Villa", "Private Phi Phi Island Yacht Charter", "Rooftop Mahanakhon Bar Pass", "All Gourmet Dinners"],
                    pnrPrefix: "CTWM-LUX-THAI"
                }
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
            imageUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
            heroTags: ["KUU Bhuntar Airport", "Parvati River", "Old Manali", "Hot Springs"],
            creatorNote: "The riverside homestay in Tosh has the clearest view of the snowline in the entire valley.",
            
            airportInfo: {
                primaryCode: "KUU",
                primaryName: "Kullu-Manali Airport (Bhuntar, Himachal)",
                alternateCode: "IXC",
                alternateName: "Chandigarh International Airport"
            },

            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹4,999",
                    budgetValue: 4999,
                    transportType: "🚌 Volvo 9600 Multi-Axle Sleeper",
                    transportDetails: "Overnight Luxury AC Volvo from Delhi Kashmere Gate / Chandigarh",
                    departureHub: "ISBT Kashmere Gate Platform 18 / Tribune Chowk",
                    arrivalStation: "Bhuntar Chowk & Kasol Riverside Drop",
                    transferMode: "5 mins scenic pine forest walk",
                    stayName: "The Hosteller Kasol / Riverside Alpine Tents",
                    stayType: "Riverside Wooden Alpine Camp & Backpacker Dorm",
                    stayAddress: "Old Chalal Trail, Kasol",
                    inclusions: ["Alpine Camp / Dorm Bed", "Kheerganga Group Trek Guide", "Nightly Campfire & Stargazing", "Local Tea Pass"],
                    pnrPrefix: "CTWM-BUD-HIM"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹11,999",
                    budgetValue: 11999,
                    transportType: "✈️ Flight to Chandigarh + 🚖 Private Mountain Cab",
                    transportDetails: "Direct Flight to IXC + Dedicated Private Dzire/Ertiga Cab",
                    departureHub: "Airport T2 (BLR) / T3 (DEL) / T2 (BOM)",
                    arrivalStation: "Chandigarh (IXC) Airport Gate 2",
                    transferMode: "Private AC Mountain Cab directly to Chalal Bridge",
                    stayName: "Parvati Woods Riverside Wooden Cottages",
                    stayType: "3-Star Attic Cedar Wood Room with Stream Balcony",
                    stayAddress: "Old Chalal Pine Forest, Kasol",
                    inclusions: ["Cedar Wood Private Cottage", "Dedicated Mountain Cab", "Kheerganga Private Guide", "Daily Mountain Breakfast"],
                    pnrPrefix: "CTWM-MID-HIM"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹22,999",
                    budgetValue: 22999,
                    transportType: "✈️ Direct Flight to Bhuntar (KUU) + 🚖 4x4 Scorpio",
                    transportDetails: "Alliance Air Direct to KUU + 4x4 Scorpio Chauffeur for all 5 Days",
                    departureHub: "IGI Delhi T2 / Airport Gateway",
                    arrivalStation: "Bhuntar (KUU) Kullu Airport Terminal",
                    transferMode: "Dedicated 4x4 Scorpio Chauffeur for all trails",
                    stayName: "Echor Palm Bliss Riverside Luxury Resort & Spa",
                    stayType: "5-Star Heated Luxury Suite facing snowcapped peaks",
                    stayAddress: "Riverside Forest Trail, Kasol",
                    inclusions: ["5-Star Heated Luxury Suite", "Dedicated 4x4 Chauffeur 24/7", "Private Naturalist Trek Guide", "All Gourmet Meals & Spa Soak"],
                    pnrPrefix: "CTWM-LUX-HIM"
                }
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
            id: "gokarna",
            name: "Gokarna Coast",
            headline: "Cliff hikes, hidden crescent coves, and acoustic campfire nights.",
            description: "4 days discovering the raw beauty of coastal Karnataka. The 5-beach cliff trek, Half Moon beach camp, secret lagoons, and oceanfront shacks.",
            vibe: "CHILL",
            duration: "4D · 3N",
            imageUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
            heroTags: ["HBX Hubballi Airport", "5 Beach Trek", "Campfire", "Beach Shacks"],
            creatorNote: "Half Moon beach is only accessible by foot or boat — totally disconnected from road traffic.",
            
            airportInfo: {
                primaryCode: "HBX",
                primaryName: "Hubballi Airport (Karnataka Gateway)",
                alternateCode: "GOI",
                alternateName: "Goa Dabolim Airport"
            },

            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹3,499",
                    budgetValue: 3499,
                    transportType: "🚆 Superfast Train / 🚌 Sleeper Bus",
                    transportDetails: "Panchaganga Superfast Express (16595) Sleeper/3AC or AC Sleeper Bus",
                    departureHub: "KSR Bengaluru (SBC) / Dadar (DR)",
                    arrivalStation: "Gokarna Road Railway Station (GOK)",
                    transferMode: "Shared Auto to Kudle Beach Top",
                    stayName: "Zostel Gokarna Cliff / Kudle Beach Bamboo Shacks",
                    stayType: "Oceanfront Cliff Dorm / Bamboo Shack",
                    stayAddress: "Kudle Beach Cliff Path, Gokarna",
                    inclusions: ["Beachfront Dorm / Shack", "5-Beach Cliff Trek Guide", "Beach Bonfire Night", "Shared Boat Ride"],
                    pnrPrefix: "CTWM-BUD-GOK"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹6,499",
                    budgetValue: 6499,
                    transportType: "✈️ Flight / 🚆 2AC Train + 🚖 Private Cab",
                    transportDetails: "Star Air to Hubballi (HBX) / 2AC Vande Bharat + Private AC Cab",
                    departureHub: "Kempegowda (BLR) / CSMIA (BOM)",
                    arrivalStation: "Hubballi (HBX) Airport / Station",
                    transferMode: "Private AC Cab directly to Kudle Hilltop",
                    stayName: "Namaste Sanjeevini Ocean Hill Stone Cottages",
                    stayType: "Curated Eco Stone Hut with Bay View",
                    stayAddress: "Kudle Hilltop Trail, Gokarna",
                    inclusions: ["Eco Stone Cottage", "Station Cab Transfers", "Scooty Rental with Helmet", "Seafood Dinner Pass"],
                    pnrPrefix: "CTWM-MID-GOK"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹16,499",
                    budgetValue: 16499,
                    transportType: "✈️ Flight + 🚖 Innova Crysta Chauffeur",
                    transportDetails: "Direct Flight to Goa/Hubballi + Dedicated Innova Chauffeur",
                    departureHub: "Airport VIP Chauffeur Lane",
                    arrivalStation: "Goa (GOX/GOI) / Hubballi Airport",
                    transferMode: "Dedicated Innova Crysta Chauffeur for all 4 days",
                    stayName: "SwaSwara - CGH Earth Ocean Wellness Resort",
                    stayType: "5-Star Private Konkan Villa surrounded by wilderness",
                    stayAddress: "Om Beach Hillside, Gokarna",
                    inclusions: ["5-Star Private Konkan Villa", "Private Boat Safari with Dolphins", "Ayurvedic Spa & Wellness Massage", "All Organic Meals"],
                    pnrPrefix: "CTWM-LUX-GOK"
                }
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
            imageUrl: "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=80",
            heroTags: ["MAA / PNY Airport", "Auroville", "Artisan Bakeries", "Cycle Crawl"],
            creatorNote: "White Town is best explored on a pastel bicycle at sunrise. Zero car honks, just birds and ocean breeze.",
            
            airportInfo: {
                primaryCode: "MAA",
                primaryName: "Chennai International Airport (2.5h scenic ECR drive)",
                alternateCode: "PNY",
                alternateName: "Puducherry Domestic Airport"
            },

            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹2,999",
                    budgetValue: 2999,
                    transportType: "🚌 Overnight Multi-Axle AC Sleeper",
                    transportDetails: "KSRTC Airavat Club Class / Private Sleeper Coach",
                    departureHub: "Madiwala St. John's / Koyambedu Chennai",
                    arrivalStation: "Pondicherry New Bus Stand (ECR)",
                    transferMode: "Vintage Bicycle Handover at Stand",
                    stayName: "Moustache Hostel White Town / Auroville Eco Guest House",
                    stayType: "Heritage Backpacker Hostel Dorm Bed",
                    stayAddress: "White Town, Puducherry",
                    inclusions: ["Hostel Dorm Bed", "Pastel Vintage Bicycle for 3 Days", "French Bakery Breakfast Pass", "Auroville Guide"],
                    pnrPrefix: "CTWM-BUD-PON"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹5,499",
                    budgetValue: 5499,
                    transportType: "✈️ Flight to Chennai (MAA) + 🚖 ECR Cab",
                    transportDetails: "Direct Flight to MAA + Pre-booked AC Sedan on scenic ECR Road",
                    departureHub: "Airport T2 (BLR) / T3 (DEL) / T2 (BOM)",
                    arrivalStation: "Chennai (MAA) Airport Terminal 1",
                    transferMode: "Private AC Cab via East Coast Road",
                    stayName: "Maison Perumal - CGH Earth French Heritage Villa",
                    stayType: "Colonial Courtyard Heritage Room",
                    stayAddress: "44, Perumal Koil St, Heritage Town",
                    inclusions: ["French Colonial Room", "ECR Highway Cab Transfers", "Vintage Bicycle Rental", "Coromandel Cafe Voucher"],
                    pnrPrefix: "CTWM-MID-PON"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹14,999",
                    budgetValue: 14999,
                    transportType: "✈️ Flight + 🚖 Mercedes / Innova Chauffeur",
                    transportDetails: "Flight to Chennai + Private Luxury Chauffeur for all 3 days",
                    departureHub: "Airport VIP Chauffeur Lane",
                    arrivalStation: "Chennai (MAA) VIP Exit Gate 4",
                    transferMode: "Dedicated Luxury Chauffeur on East Coast Road",
                    stayName: "Palais de Mahé - CGH Earth 5-Star Mansion",
                    stayType: "5-Star French Colonial Mansion Suite with Pool",
                    stayAddress: "Bussy Street, White Town, Puducherry",
                    inclusions: ["5-Star Mansion Suite", "Dedicated Luxury Chauffeur 24/7", "Private Auroville Naturalist Guide", "Gourmet French-Tamil Dinners"],
                    pnrPrefix: "CTWM-LUX-PON"
                }
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
            imageUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80",
            heroTags: ["KLIA Airport", "Penang Hawkers", "Batu Caves", "UNESCO Murals"],
            creatorNote: "The KTM train from KL Sentral to Butterworth is faster and more comfortable than flying.",
            
            airportInfo: {
                primaryCode: "KLIA",
                primaryName: "Kuala Lumpur International Airport",
                alternateCode: "PEN",
                alternateName: "Penang International Airport"
            },

            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹12,999",
                    budgetValue: 12999,
                    transportType: "✈️ Economy Flight + 🚆 KL Express & KTM Train",
                    transportDetails: "Batik Air / AirAsia Economy + KTM Electric Train to Penang",
                    departureHub: "T2 / T3 International Terminal",
                    arrivalStation: "KLIA Terminal 2 / Penang Sentral",
                    transferMode: "KL Monorail Pass & George Town Walking Tour",
                    stayName: "The Bed KLCC Pod & Georgetown Heritage Hostel",
                    stayType: "Modern Capsule Pod & UNESCO Heritage Dorm",
                    stayAddress: "Jalan Sultan Ismail & Chulia Street",
                    inclusions: ["Capsule Pod Bed", "KTM Electric Train Ticket", "Jalan Alor Hawker Food Voucher", "Batu Caves Metro Pass"],
                    pnrPrefix: "CTWM-BUD-MAL"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹21,999",
                    budgetValue: 21999,
                    transportType: "✈️ Direct Flight + 🚆 ETS Platinum Train",
                    transportDetails: "Malaysia Airlines Direct Flight + ETS Platinum Class",
                    departureHub: "T2 / T3 International Airport",
                    arrivalStation: "KLIA Terminal 1 Arrivals",
                    transferMode: "Pre-loaded Grab Cab Wallet & Airport Express",
                    stayName: "The FACE Suites KL & Cheong Fatt Tze Blue Mansion",
                    stayType: "1-Bedroom Skyline Suite with Petronas View",
                    stayAddress: "1020 Jalan Sultan Ismail & George Town",
                    inclusions: ["Skyline Infinity Pool Suite", "ETS Platinum Train Ticket", "Daily Breakfasts", "Batu Caves Private Cab"],
                    pnrPrefix: "CTWM-MID-MAL"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹44,999",
                    budgetValue: 44999,
                    transportType: "✈️ Business Class Flight + 🚖 Luxury Vellfire MPV",
                    transportDetails: "Malaysia Airlines Business Class + Dedicated Private Vellfire MPV",
                    departureHub: "VIP Business Lounge",
                    arrivalStation: "KLIA VIP Fast-Track Gate",
                    transferMode: "Dedicated Toyota Vellfire Chauffeur for KL and Penang",
                    stayName: "Banyan Tree Kuala Lumpur & Eastern & Oriental 5-Star Hotel",
                    stayType: "5-Star Luxury Suite facing Petronas Towers",
                    stayAddress: "Jalan Conlay, KL & Farquhar St, Penang",
                    inclusions: ["5-Star Luxury Suites", "Dedicated Vellfire MPV Chauffeur 24/7", "Vertigo Rooftop VIP Lounge Pass", "Private Michelin Hawker Food Tour"],
                    pnrPrefix: "CTWM-LUX-MAL"
                }
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
        },
        {
            id: "krabi",
            name: "Krabi Island Escapes",
            headline: "The kind of turquoise water that breaks your camera settings.",
            description: "5 days in paradise. Railay peninsula cliffs, 4 Islands longtail cruise, emerald freshwater lagoons, and sunset beach seafood barbecues.",
            vibe: "LUXURY",
            duration: "5D · 4N",
            imageUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
            heroTags: ["KBV Krabi Airport", "Railay Cliffs", "Emerald Pool", "Sunset BBQ"],
            creatorNote: "We booked a private traditional longtail with local captain Somchai — no loudspeaker tour guides.",
            
            airportInfo: {
                primaryCode: "KBV",
                primaryName: "Krabi International Airport",
                alternateCode: "HKT",
                alternateName: "Phuket International Airport"
            },

            tiers: {
                "budget": {
                    tierName: "🎒 Budget Backpacker",
                    price: "₹15,999",
                    budgetValue: 15999,
                    transportType: "✈️ Connecting Economy Flight + 🚤 Longtail",
                    transportDetails: "AirAsia Flight + Shared Airport Van & Traditional Longtail",
                    departureHub: "T2 / T3 International Airport",
                    arrivalStation: "Krabi Airport (KBV) / Ao Nang Beach",
                    transferMode: "Shared Longtail Boat to Railay West",
                    stayName: "Blanco Beach Bar & Hostel / Railay Eco Bamboo Bungalow",
                    stayType: "Beachfront Backpacker Pod & Bamboo Hut",
                    stayAddress: "Railay Beach Peninsula",
                    inclusions: ["Beachfront Pod / Hut", "4 Islands Shared Tour", "Railay Rock Climbing Pass", "Sunset Beach Bar Pass"],
                    pnrPrefix: "CTWM-BUD-KRB"
                },
                "mid": {
                    tierName: "✨ Mid-Tier Best Value",
                    price: "₹28,999",
                    budgetValue: 28999,
                    transportType: "✈️ Direct Flight + 🚖 Van & Private Longtail",
                    transportDetails: "IndiGo / Thai Airways Flight + Private AC Van to Pier",
                    departureHub: "T2 / T3 International Airport",
                    arrivalStation: "Krabi (KBV) Airport Gate 2",
                    transferMode: "Private Van & Private Traditional Longtail Charter",
                    stayName: "Railay Bay Resort & Spa Deluxe Cottages",
                    stayType: "4-Star Beachfront Deluxe Cottage",
                    stayAddress: "145 M.2 Ao Nang, Railay Beach",
                    inclusions: ["Deluxe Beachfront Cottage", "Private 4-Islands Longtail Boat", "Daily Buffet Breakfasts", "Ao Nang Seafood Dinner Pass"],
                    pnrPrefix: "CTWM-MID-KRB"
                },
                "luxury": {
                    tierName: "🌟 Luxury Creator Escape",
                    price: "₹54,999",
                    budgetValue: 54999,
                    transportType: "✈️ Premium Business Flight + 🛥️ Private Yacht",
                    transportDetails: "Business Class Flight + Private Speedboat Charter from Pier",
                    departureHub: "Airport VIP Lounge",
                    arrivalStation: "Krabi VIP Chauffeur Reception",
                    transferMode: "Private Luxury Speedboat Charter direct to Resort Jetty",
                    stayName: "Rayavadee 5-Star Luxury Pavilion & Pool Villa",
                    stayType: "5-Star Private Luxury Pavilion surrounded by limestone cliffs",
                    stayAddress: "214 Moo 2, Tambon Ao-Nang, Railay",
                    inclusions: ["5-Star Luxury Pool Pavilion", "Private Speedboat Charter to Phi Phi & Hong Islands", "The Grotto Cave Private Dinner", "All Fine Dining & Spa"],
                    pnrPrefix: "CTWM-LUX-KRB"
                }
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
        }
    ],
    videoProofs: [
        {
            id: "v1",
            title: "ComeTripWithMe: Real Trips, Real Proof (Watch Before You Book)",
            destination: "Luxury & Budget Segments",
            duration: "14:20",
            views: "45K views",
            thumbnailUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
            videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            highlights: ["5-Star Resorts vs Zostel Dorms", "Innova Cabs vs Sleeper Buses", "Real street prices", "Local contacts"]
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
            tripTag: "🌟 Luxury Tier · Goa Cliff Escape",
            rating: 5,
            reviewQuote: "Booked the Luxury tier with flight from BLR and private Innova Crysta. The 5-star Thalassa villa and private table was seamless. Didn't have to think about a single thing."
        },
        {
            id: "r2",
            authorHandle: "@arjun_wanders",
            city: "Delhi",
            tripTag: "🎒 Budget Tier · Gokarna Beach Trail",
            rating: 5,
            reviewQuote: "Took the budget tier with sleeper coach and Zostel cliff dorm for ₹3,499. Met insane creators on the cliff trail. Real proof, no tourist traps."
        },
        {
            id: "r3",
            authorHandle: "@priya.irl",
            city: "Mumbai",
            tripTag: "✨ Mid-Tier · Thailand & Krabi",
            rating: 5,
            reviewQuote: "Mid-tier package was the best value imaginable. ASAI Chinatown was gorgeous, and the private longtail boat to 4-islands beat crowded tours by a mile."
        }
    ],
    packingItems: [
        { id: "p1", title: "Govt ID / Passport & Flight / Bus / Train Ticket", category: "Essentials", isChecked: true },
        { id: "p2", title: "Power Bank (min 10,000 mAh for transit)", category: "Tech", isChecked: false },
        { id: "p3", title: "Comfortable travel shoes & beach sandals", category: "Apparel", isChecked: false },
        { id: "p4", title: "Sunscreen SPF 50+ & Sunglasses", category: "Care", isChecked: true },
        { id: "p5", title: "Quick-dry towel & Swimwear", category: "Apparel", isChecked: false },
        { id: "p6", title: "Offline downloaded maps & playlist", category: "Tech", isChecked: false }
    ],
    wishlist: ["goa", "thailand"]
};

// State Manager
class AppStore {
    constructor() {
        const saved = localStorage.getItem('cometrip_store_data_v4');
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
        this.selectedTierFilter = 'ALL'; // 'ALL', 'budget', 'mid', 'luxury'
        this.activeTripTiers = {}; // tripId -> 'budget' | 'mid' | 'luxury'
        
        // Initialize default tiers for all trips
        this.data.trips.forEach(t => {
            this.activeTripTiers[t.id] = 'mid';
        });

        this.activeTab = 'explore';
        this.activeGuideTripId = 'goa';
        this.activeGuideDayIndex = 0;
        this.timelineScrubIndex = 0;
        this.visitedStops = new Set();
        this.activeAudioStory = null;
        this.isPlayingAudio = false;
        this.speechRate = 1.0;
        this.speechUtterance = null;
        this.selectedReelsChannel = 'ALL';
    }

    save() {
        localStorage.setItem('cometrip_store_data_v4', JSON.stringify(this.data));
    }

    getTrip(id) {
        return this.data.trips.find(t => t.id.toLowerCase() === id.toLowerCase()) || this.data.trips[0];
    }

    getTripTier(tripId) {
        return this.activeTripTiers[tripId] || 'mid';
    }

    setTripTier(tripId, tier) {
        this.activeTripTiers[tripId] = tier;
        renderExploreTrips();
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

// Set Global Origin City (BLR / DEL / BOM)
function setGlobalOriginCity(originCode) {
    store.selectedOrigin = originCode;
    store.data.userBooking.departureOrigin = originCode;
    store.save();

    document.querySelectorAll('.origin-city-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.getElementById('originBtn-' + originCode);
    if (activeBtn) activeBtn.classList.add('active');

    const org = store.data.origins[originCode] || store.data.origins['BLR'];
    const heroTag = document.getElementById('heroOriginTag');
    if (heroTag) heroTag.textContent = `✦ DEPARTING FROM ${org.name.toUpperCase()} (${org.code}) · LUXURY · MID · BUDGET`;
    
    const spotOrigin = document.getElementById('spotlightOriginName');
    if (spotOrigin) spotOrigin.textContent = `${org.name} (${org.code})`;

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

// RENDER: EXPLORE SCREEN WITH 3-TIER SEGMENTS
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
    if (store.selectedTierFilter !== 'ALL') {
        // Just sets the visual tier on all cards
        filtered.forEach(t => store.activeTripTiers[t.id] = store.selectedTierFilter);
    }

    container.innerHTML = filtered.map(t => {
        const isSaved = store.isWishlisted(t.id);
        const activeTierKey = store.getTripTier(t.id);
        const tier = t.tiers[activeTierKey] || t.tiers['mid'];
        const ap = t.airportInfo;

        return `
            <div class="trip-card" onclick="openTripDetailModal('${t.id}')">
                <div class="trip-card-image-wrap">
                    <img src="${t.imageUrl}" class="trip-card-image" alt="${t.name}">
                    <div class="trip-card-overlay-top">
                        <span class="airport-hub-badge"><i class="fa-solid fa-plane-arrival"></i> ${ap ? ap.primaryCode : 'AIR'} Gateway</span>
                        <button class="wishlist-heart-btn ${isSaved ? 'is-saved' : ''}" onclick="event.stopPropagation(); store.toggleWishlist('${t.id}')">
                            <i class="fa-${isSaved ? 'solid' : 'regular'} fa-heart"></i>
                        </button>
                    </div>
                    <div class="trip-card-overlay-bottom">
                        <span class="trip-price-pill">${tier.price}</span>
                        <span class="trip-duration-pill">${t.duration}</span>
                    </div>
                </div>
                <div class="trip-card-body">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <h3 class="trip-card-title">${t.name}</h3>
                        <span class="tier-badge ${activeTierKey}">${tier.tierName.split(' ')[0]}</span>
                    </div>
                    
                    <div class="trip-card-headline">${t.headline}</div>
                    
                    <!-- Interactive 3-Tier Switcher Pill -->
                    <div class="tier-pill-selector" onclick="event.stopPropagation();">
                        <button class="tier-pill-btn ${activeTierKey === 'budget' ? 'active-tier-budget' : ''}" onclick="store.setTripTier('${t.id}', 'budget')">
                            🎒 Budget
                        </button>
                        <button class="tier-pill-btn ${activeTierKey === 'mid' ? 'active-tier-mid' : ''}" onclick="store.setTripTier('${t.id}', 'mid')">
                            ✨ Mid-Tier
                        </button>
                        <button class="tier-pill-btn ${activeTierKey === 'luxury' ? 'active-tier-luxury' : ''}" onclick="store.setTripTier('${t.id}', 'luxury')">
                            🌟 Luxury
                        </button>
                    </div>

                    <!-- Dynamic Tier Logistics Summary Box -->
                    <div style="background:rgba(15, 25, 45, 0.6); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:8px 10px; margin-bottom:10px; font-size:11px;">
                        <div style="color:var(--gold-light); font-weight:700; margin-bottom:2px;">
                            ${tier.transportType}
                        </div>
                        <div style="color:var(--text-secondary); font-size:10px;">
                            🏨 <strong>Stay:</strong> ${tier.stayName}
                        </div>
                    </div>

                    <p class="trip-card-desc">${t.description}</p>
                    <div class="trip-card-tags">
                        ${tier.inclusions.slice(0, 3).map(inc => `<span class="tag-pill">✓ ${inc}</span>`).join('')}
                    </div>
                    <div class="trip-card-footer">
                        <span style="font-size:11px; color:var(--gold-primary); font-weight:700;">✦ ${activeTierKey.toUpperCase()} Plan</span>
                        <span class="gold-btn" style="padding:6px 14px; font-size:11px;">Book & View ➔</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function filterTripsBySegment(segmentKey, btn) {
    store.selectedTierFilter = segmentKey;
    document.querySelectorAll('#segmentFilterChips .filter-chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    
    if (segmentKey !== 'ALL') {
        store.data.trips.forEach(t => store.activeTripTiers[t.id] = segmentKey);
    }
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
    const tier = document.getElementById('smartTierSelect').value;
    const org = store.selectedOrigin;
    const orgData = store.data.origins[org] || store.data.origins['BLR'];

    let recTitle = "Curated Flight & Stay Route";
    let recSub = `Handcrafted itinerary matched for ${orgData.name} in the ${tier.toUpperCase()} class.`;

    if (tier === 'budget') {
        recTitle = `🎒 Budget Explorer — From ₹2,999/person (${orgData.code})`;
        recSub = `Overnight AC Sleeper Bus / Train + Social Backpacker Hostel (Zostel) + Self-Drive Scooty pass.`;
    } else if (tier === 'mid') {
        recTitle = `✨ Mid-Tier Best Value — From ₹6,499 - ₹8,999 (${orgData.code})`;
        recSub = `Direct Flight + AC Cab transfer + Curated Boutique Hotel + Cafe breakfasts & audio guide.`;
    } else if (tier === 'luxury') {
        recTitle = `🌟 Luxury Creator Escape — From ₹18,999+ (${orgData.code})`;
        recSub = `Premium Direct Flight + Dedicated Innova Crysta Chauffeur + 5-Star Oceanfront Villa + VIP Sunset tables.`;
    }

    document.getElementById('smartResultTitle').textContent = recTitle;
    document.getElementById('smartResultSub').textContent = recSub;
}

function viewSmartMatchedTrip() {
    const dest = "goa";
    openTripDetailModal(dest);
}

function inquireSmartMatchWhatsApp() {
    const tier = document.getElementById('smartTierSelect').value;
    const org = store.selectedOrigin;
    const budget = document.getElementById('smartBudgetVal').textContent;
    const title = document.getElementById('smartResultTitle').textContent;

    const msg = `Hey ComeTripWithMe! ✦ I'm interested in the *${tier.toUpperCase()}* segment trip:\n\n` +
                `🛫 Departing From: ${org} (${store.data.origins[org].name})\n` +
                `✨ Travel Class: ${tier.toUpperCase()} (Flight/Bus/Train + Stays)\n` +
                `💰 Budget Target: ${budget}/person\n` +
                `📋 Selected Route: ${title}\n\n` +
                `Please share available departure slots and booking details!`;

    openWhatsAppLink(msg);
}

// TRIP DETAIL MODAL WITH 3-TIER SEGMENT LOGISTICS
function openTripDetailModal(tripId) {
    const trip = store.getTrip(tripId);
    if (!trip) return;

    document.getElementById('modalTripName').textContent = trip.name;
    const body = document.getElementById('modalTripBody');
    const isSaved = store.isWishlisted(trip.id);
    const ap = trip.airportInfo;
    const activeTierKey = store.getTripTier(trip.id);
    const tier = trip.tiers[activeTierKey] || trip.tiers['mid'];

    body.innerHTML = `
        <div style="width:100%; height:200px; border-radius:var(--radius-lg); overflow:hidden; position:relative; margin-bottom:16px;">
            <img src="${trip.imageUrl}" style="width:100%; height:100%; object-fit:cover;" alt="${trip.name}">
            <div style="position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(7,9,14,0.9) 100%); padding:16px; display:flex; flex-direction:column; justify-content:flex-end;">
                <div style="display:flex; gap:6px; margin-bottom:4px;">
                    <span class="airport-hub-badge"><i class="fa-solid fa-plane-arrival"></i> ${ap ? ap.primaryCode : 'DEST'} Gateway</span>
                    <span class="tier-badge ${activeTierKey}">${tier.tierName}</span>
                </div>
                <h2 style="font-family:var(--font-heading); font-size:20px; font-weight:900; color:#fff;">${trip.headline}</h2>
            </div>
        </div>

        <!-- 3-Way Tier Selector in Modal -->
        <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:12px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:11px; font-weight:800; color:var(--gold-light);">Choose Travel Class:</span>
                <span class="trip-price-pill" style="font-size:13px;">${tier.price}</span>
            </div>
            <div class="tier-pill-selector" style="margin:0;">
                <button class="tier-pill-btn ${activeTierKey === 'budget' ? 'active-tier-budget' : ''}" onclick="store.setTripTier('${trip.id}', 'budget'); openTripDetailModal('${trip.id}');">
                    🎒 Budget (Hostel+Bus)
                </button>
                <button class="tier-pill-btn ${activeTierKey === 'mid' ? 'active-tier-mid' : ''}" onclick="store.setTripTier('${trip.id}', 'mid'); openTripDetailModal('${trip.id}');">
                    ✨ Mid-Tier (Boutique+Flight)
                </button>
                <button class="tier-pill-btn ${activeTierKey === 'luxury' ? 'active-tier-luxury' : ''}" onclick="store.setTripTier('${trip.id}', 'luxury'); openTripDetailModal('${trip.id}');">
                    🌟 Luxury (5-Star+Cab)
                </button>
            </div>
        </div>

        <!-- Tier Transport Logistics Card -->
        <div class="transit-hub-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span class="transit-badge"><i class="fa-solid fa-route"></i> ${tier.transportType}</span>
                <span style="font-family:var(--font-mono); font-size:11px; color:#7DD3FC;">PNR: ${tier.pnrPrefix}-${store.selectedOrigin}</span>
            </div>
            <div style="font-size:12px; font-weight:800; color:#fff;">${tier.transportDetails}</div>
            <div style="font-size:11px; color:var(--gold-light); margin-top:2px;">📍 <strong>Departure:</strong> ${tier.departureHub}</div>
            <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">🛬 <strong>Arrival & Transfer:</strong> ${tier.arrivalStation} (${tier.transferMode})</div>
        </div>

        <!-- Tier Accommodation Card -->
        <div class="hotel-hub-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span class="hotel-badge"><i class="fa-solid fa-hotel"></i> ${tier.stayType}</span>
                <span style="font-size:10px; color:#D8B4FE; font-weight:700;">Check-in: 11:00 AM</span>
            </div>
            <h4 style="font-family:var(--font-heading); font-size:15px; font-weight:800; color:#fff;">${tier.stayName}</h4>
            <p style="font-size:11px; color:var(--text-secondary); margin-bottom:8px;">📍 ${tier.stayAddress}</p>
            <div style="background:rgba(0,0,0,0.3); padding:8px 12px; border-radius:var(--radius-md);">
                <div style="font-size:11px; font-weight:700; color:var(--gold-light); margin-bottom:4px;">Inclusions in this Tier:</div>
                <div style="display:flex; flex-wrap:wrap; gap:6px;">
                    ${tier.inclusions.map(inc => `<span class="tag-pill">✓ ${inc}</span>`).join('')}
                </div>
            </div>
        </div>

        <!-- Creator Note -->
        <div class="insider-tip-box" style="margin-bottom:18px;">
            <strong>✦ Creator Field Note:</strong> ${trip.creatorNote}
        </div>

        <!-- Day-by-Day Breakdown -->
        <h3 class="section-title" style="margin-bottom:12px;"><span class="sparkle">✦</span> Verified Route Itinerary</h3>
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
                <i class="fa-solid fa-ticket"></i> Book ${tier.tierName.split(' ')[0]} (${tier.price}) & Activate Pass
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

// REAL-TIME DIGITAL BOARDING PASS WITH 3 TIERS
function bookTripAndActivateLivePass(tripId) {
    const trip = store.getTrip(tripId);
    const tierKey = store.getTripTier(trip.id);
    const tier = trip.tiers[tierKey] || trip.tiers['mid'];

    store.data.userBooking.bookedTripId = trip.id;
    store.data.userBooking.selectedTier = tierKey;
    store.data.userBooking.departureOrigin = store.selectedOrigin;
    store.data.userBooking.bookingId = `CTWM-${tierKey.toUpperCase()}-${store.selectedOrigin}-${Math.floor(1000 + Math.random() * 9000)}`;
    store.save();
    
    closeModal('tripDetailModal');
    showToast(`🎉 ${tier.tierName} Booked from ${store.selectedOrigin}! Live Boarding Pass Generated ✦`);
    openActiveBoardingPassModal();
}

function openActiveBoardingPassModal() {
    const b = store.data.userBooking;
    const trip = store.getTrip(b.bookedTripId || 'goa');
    const tierKey = b.selectedTier || 'mid';
    const tier = trip.tiers[tierKey] || trip.tiers['mid'];
    const org = store.selectedOrigin || b.departureOrigin || 'BLR';

    document.getElementById('passModalTripName').textContent = trip.name;
    const body = document.getElementById('passModalBody');

    body.innerHTML = `
        <div class="boarding-pass-card">
            <div class="boarding-pass-header">
                <div>
                    <span style="font-size:9px; font-weight:900; letter-spacing:1px; text-transform:uppercase;">OFFICIAL ${tierKey.toUpperCase()} PASS · ${org} ➔ ${trip.airportInfo.primaryCode}</span>
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
                        <div class="ticket-label">Tier & Transport</div>
                        <div class="ticket-val mono" style="font-size:13px; color:#38BDF8;">${tier.tierName}</div>
                        <div style="font-size:10px; color:var(--text-muted);">${tier.transportType}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Booking Reference / PNR</div>
                        <div class="ticket-val mono">${b.bookingId}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Departure Hub & Point</div>
                        <div class="ticket-val" style="font-size:12px;">${tier.departureHub}</div>
                    </div>
                    <div>
                        <div class="ticket-label">Arrival & Accommodation</div>
                        <div class="ticket-val" style="color:var(--gold-light); font-size:12px;">${tier.stayName}</div>
                        <div style="font-size:10px; color:#86EFAC;">● CONFIRMED & ACTIVE</div>
                    </div>
                </div>

                <div class="ticket-perforated-divider"></div>

                <!-- Live Tier Voucher Breakdown -->
                <div style="display:flex; flex-direction:column; gap:10px;">
                    <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-size:11px; font-weight:800; color:#7DD3FC;"><i class="fa-solid fa-ticket"></i> Transport Voucher</span>
                            <span style="font-size:10px; color:var(--gold-light); font-weight:700;">${tier.price}</span>
                        </div>
                        <div style="font-size:11px; color:var(--text-secondary);">
                            ${tier.transportDetails}<br>
                            📍 Transfer: ${tier.transferMode}
                        </div>
                    </div>

                    <div style="background:var(--bg-dark); border:1px solid var(--glass-border); border-radius:var(--radius-md); padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-size:11px; font-weight:800; color:#D8B4FE;"><i class="fa-solid fa-hotel"></i> Stay Voucher</span>
                            <span style="font-size:10px; color:#D8B4FE; font-weight:700;">Check-in: 11:00 AM</span>
                        </div>
                        <div style="font-size:11px; color:var(--text-secondary);">
                            🏨 ${tier.stayName} (${tier.stayType})<br>
                            📍 ${tier.stayAddress}
                        </div>
                    </div>
                </div>

                <!-- Barcode -->
                <div style="margin-top:16px; text-align:center;">
                    <div style="font-family:var(--font-mono); font-size:24px; letter-spacing:4px; color:var(--gold-primary);">|||| | ||||| || |||||| | |||</div>
                    <div style="font-size:9px; color:var(--text-muted); letter-spacing:1px; margin-top:2px;">OFFICIAL DIGITAL COMPANION PASS · VALID FOR ALL INCLUSIONS</div>
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
    const tierKey = store.getTripTier(trip.id);
    const tier = trip.tiers[tierKey] || trip.tiers['mid'];

    transitHub.innerHTML = `
        <div class="transit-hub-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span class="transit-badge"><i class="fa-solid fa-route"></i> ${tier.tierName}</span>
                <span style="font-size:10px; color:#86EFAC; font-weight:700;">${tier.price}</span>
            </div>
            <div style="font-size:12px; font-weight:800; color:#fff;">${tier.transportType}</div>
            <div style="font-size:11px; color:var(--gold-light); margin-top:2px;">📍 <strong>Dep Point:</strong> ${tier.departureHub}</div>
            <div style="font-size:11px; color:var(--text-secondary); margin-top:4px;">🛬 <strong>Arrival & Transfer:</strong> ${tier.arrivalStation} (${tier.transferMode})</div>
        </div>

        <div class="hotel-hub-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span class="hotel-badge"><i class="fa-solid fa-hotel"></i> ${tier.stayType}</span>
                <span style="font-size:10px; color:#D8B4FE; font-weight:700;">Check-in: 11:00 AM</span>
            </div>
            <div style="font-size:12px; font-weight:800; color:#fff;">🏨 ${tier.stayName}</div>
            <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">📍 ${tier.stayAddress}</div>
            
            <div style="border-top:1px solid rgba(168, 85, 247, 0.2); padding-top:8px; margin-top:8px; display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:10px; color:var(--text-muted);">Inclusions: ${tier.inclusions.slice(0, 2).join(' · ')}</div>
                <a href="https://maps.google.com/?q=${encodeURIComponent(tier.stayName)}" target="_blank" class="gold-badge" style="font-size:9px; text-decoration:none;">
                    <i class="fa-solid fa-location-arrow"></i> Map
                </a>
            </div>
        </div>
    `;

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
    const tierKey = store.getTripTier(trip.id);
    const tier = trip.tiers[tierKey] || trip.tiers['mid'];

    const stages = [
        { pill: `🟢 LIVE · DEPARTURE FROM ${org}`, time: "06:00 AM", title: `🛫 ${tier.departureHub}`, desc: `${tier.transportType} departure in progress.` },
        { pill: `🛬 LIVE · ARRIVAL & LOCAL TRANSFER`, time: "08:15 AM", title: `📍 ${tier.arrivalStation}`, desc: `Transfer via ${tier.transferMode}.` },
        { pill: `🏨 LIVE · CHECK-IN AT ${tier.stayName}`, time: "11:00 AM", title: `🏨 ${tier.stayName}`, desc: `Check-in completed. ${tier.stayType}.` },
        { pill: "🌅 LIVE · EVENING CLIFF SUNDOWNER", time: "05:30 PM", title: "🌅 Golden Hour Sunset & Creator Food Trail", desc: "Golden hour sunset light over the bay. Reserved table ready." },
        { pill: "🌌 LIVE · NIGHT TRAIL & DINNER", time: "09:00 PM", title: "🍲 Food Crawl & Local Vibes", desc: "Creator verified dinner spots & local night trail." }
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
        { x: 165, y: 65, name: "🏨 Stay", icon: "hotel" },
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

    document.getElementById('mapInfoBadge').innerHTML = `<i class="fa-solid fa-route"></i> Route: ${org} ➔ Stay ➔ ${stops.length} Waypoints`;
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
    const tier = document.querySelector('input[name="plannerTier"]:checked').value;
    const dest = document.getElementById('planDestSelect').value;
    const squad = document.getElementById('planSquadSelect').value;
    const date = document.getElementById('planDateInput').value || 'Flexible / Upcoming Friday';
    const budget = document.getElementById('planBudgetInput').value || 'Standard Tier';
    const notes = document.getElementById('planNotesInput').value || 'None';

    const msg = `✦ *NEW TRIP INQUIRY — ComeTripWithMe* ✦\n\n` +
                `🛫 *Departing From:* ${orgData.name} (${orgData.code})\n` +
                `✨ *Travel Class:* ${tier}\n` +
                `📍 *Destination:* ${dest}\n` +
                `👥 *Squad Size:* ${squad}\n` +
                `🗓️ *Dates:* ${date}\n` +
                `💰 *Budget Target:* ${budget}\n` +
                `📝 *Stay & Transit Preferences:* ${notes}\n\n` +
                `Please send available dates and the verified itinerary!`;

    openWhatsAppLink(msg);
}

function sendCustomPlannerEmail() {
    const org = store.selectedOrigin;
    const dest = document.getElementById('planDestSelect').value;
    const squad = document.getElementById('planSquadSelect').value;
    const subject = encodeURIComponent(`Booking Inquiry: ${org} to ${dest} for ${squad}`);
    const body = encodeURIComponent(`Hi ComeTripWithMe team,\n\nI want to plan a custom trip from ${org} to ${dest}.\nPlease share available options for Luxury, Mid-Tier, and Budget classes.\n\nThank you!`);
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
        const tier = trip.tiers['mid'] || Object.values(trip.tiers)[0];
        return `
            <div class="trip-card" style="margin-bottom:12px;" onclick="openTripDetailModal('${trip.id}')">
                <div style="display:flex; align-items:center; gap:12px; padding:12px;">
                    <img src="${trip.imageUrl}" style="width:70px; height:70px; border-radius:var(--radius-md); object-fit:cover;" alt="${trip.name}">
                    <div style="flex:1;">
                        <h4 style="font-size:14px; font-weight:800; color:#fff;">${trip.name}</h4>
                        <div style="font-size:11px; color:var(--gold-primary); font-weight:700;">${tier.price} · ${trip.duration}</div>
                        <span class="vibe-badge vibe-${trip.vibe.toLowerCase()}" style="font-size:9px; margin-top:4px;">${trip.vibe}</span>
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
        const tiers = t.tiers || {};
        return `
            <div class="glass-panel" style="padding:14px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <h4 style="font-size:14px; font-weight:800; color:#fff;">${t.name} Tiers</h4>
                        <span style="font-size:10px; color:var(--gold-primary);">Luxury: ${tiers.luxury ? tiers.luxury.price : ''} · Mid: ${tiers.mid ? tiers.mid.price : ''} · Budget: ${tiers.budget ? tiers.budget.price : ''}</span>
                    </div>
                    <button class="gold-badge" onclick="promptEditTripTiers('${t.id}')">
                        <i class="fa-solid fa-pen"></i> Edit Pricing
                    </button>
                </div>
                <div style="font-size:11px; color:var(--text-secondary); line-height:1.4;">
                    🌟 <strong>Luxury:</strong> ${tiers.luxury ? tiers.luxury.stayName : 'Resort'} (${tiers.luxury ? tiers.luxury.transportType : 'Flight'})<br>
                    ✨ <strong>Mid-Tier:</strong> ${tiers.mid ? tiers.mid.stayName : 'Hotel'} (${tiers.mid ? tiers.mid.transportType : 'Flight/Cab'})<br>
                    🎒 <strong>Budget:</strong> ${tiers.budget ? tiers.budget.stayName : 'Hostel'} (${tiers.budget ? tiers.budget.transportType : 'Bus/Train'})
                </div>
            </div>
        `;
    }).join('');
}

function promptEditTripTiers(tripId) {
    const t = store.getTrip(tripId);
    const newBudgetPrice = prompt("Budget Tier Price (e.g. ₹3,999):", t.tiers.budget.price);
    if (newBudgetPrice) t.tiers.budget.price = newBudgetPrice;

    const newMidPrice = prompt("Mid-Tier Price (e.g. ₹8,999):", t.tiers.mid.price);
    if (newMidPrice) t.tiers.mid.price = newMidPrice;

    const newLuxPrice = prompt("Luxury Tier Price (e.g. ₹18,999):", t.tiers.luxury.price);
    if (newLuxPrice) t.tiers.luxury.price = newLuxPrice;

    store.save();
    renderExploreTrips();
    renderCmsTransitEditor();
    showToast(`Updated tier pricing for ${t.name} ✦`);
}

function renderCmsTripsList() {
    const container = document.getElementById('cmsTripsListContainer');
    container.innerHTML = store.data.trips.map(t => `
        <div class="glass-panel" style="padding:12px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <h4 style="font-size:13px; font-weight:800; color:#fff;">${t.name} (${t.duration})</h4>
                <span class="gold-badge" style="font-size:10px;">${t.tiers.mid ? t.tiers.mid.price : '₹8,999'}</span>
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
    const newHeadline = prompt("Headline:", t.headline);

    t.name = newName;
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
    const id = name.toLowerCase().replace(/[^a-z0-9]/g, '_');

    const newTrip = {
        id: id,
        name: name,
        headline: "Handcrafted creator route, coffee estates & misty peaks.",
        description: `Verified 3-day itinerary exploring the hidden gems and secret trails of ${name}.`,
        vibe: "CHILL",
        duration: "3D · 2N",
        imageUrl: "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?w=800&q=80",
        heroTags: [name, "Creator Verified", "Coffee Estates"],
        creatorNote: "Scouted and verified by ComeTripWithMe.",
        airportInfo: { primaryCode: "MYQ", primaryName: "Mysore / BLR Gateway" },
        tiers: {
            "budget": { tierName: "🎒 Budget Backpacker", price: "₹2,999", transportType: "🚌 AC Sleeper Bus", transportDetails: "KSRTC Multi-Axle Bus", departureHub: "Satellite ISBT", arrivalStation: `${name} Bus Stand`, transferMode: "Scooty Handover", stayName: "Zostel Coorg / Plantation Dorm", stayType: "Plantation Hostel Dorm", stayAddress: `${name} Estate Rd`, inclusions: ["Dorm Bed", "Scooty with Helmet", "Coffee Trail Walk"], pnrPrefix: `CTWM-BUD-${id.toUpperCase()}` },
            "mid": { tierName: "✨ Mid-Tier Best Value", price: "₹6,499", transportType: "🚖 Private AC Highway Cab", transportDetails: "Private AC Ertiga/Dzire directly from Bengaluru/Mysore", departureHub: "Doorstep Pickup / Airport Gateway", arrivalStation: `${name} Villa`, transferMode: "Private AC Cab for 3 Days", stayName: "Misty Plantation Estate Villa", stayType: "3-Star Boutique Cottage", stayAddress: "Coffee Estate, Karnataka", inclusions: ["Private Plantation Cottage", "Private Cab", "Estate Breakfasts"], pnrPrefix: `CTWM-MID-${id.toUpperCase()}` },
            "luxury": { tierName: "🌟 Luxury Creator Escape", price: "₹16,999", transportType: "🚖 Innova Crysta Chauffeur", transportDetails: "Dedicated Luxury Innova Crysta Chauffeur for all 3 days", departureHub: "VIP Doorstep Chauffeur", arrivalStation: "Resort Portico", transferMode: "Dedicated Innova Chauffeur 24/7", stayName: "Evolve Back Luxury Plantation Resort", stayType: "5-Star Private Pool Villa", stayAddress: `${name} Luxury Enclave`, inclusions: ["5-Star Private Pool Villa", "Dedicated Innova Chauffeur", "Private Plantation Naturalist", "All Gourmet Meals"], pnrPrefix: `CTWM-LUX-${id.toUpperCase()}` }
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
    store.activeTripTiers[id] = 'mid';
    store.save();
    renderExploreTrips();
    renderCmsTripsList();
    showToast(`✦ Added new trip: ${name}!`);
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
    dlAnchor.setAttribute("download", "cometripwithme_tiered_app_database.json");
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
    openWhatsAppLink(`Hey ComeTripWithMe! ✦ I'd like to plan a trip departing from ${org}.`);
}

function inquireTripWhatsApp(tripId) {
    const trip = store.getTrip(tripId);
    const org = store.selectedOrigin;
    const tierKey = store.getTripTier(trip.id);
    const tier = trip.tiers[tierKey] || trip.tiers['mid'];
    const msg = `Hey ComeTripWithMe! ✦ I'm interested in booking the *${trip.name}* trip in the *${tier.tierName}* segment (${tier.price}) departing from *${org}* (${tier.transportType}). Can you share available departure dates?`;
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
    toast.innerHTML = `<i class="fa-solid fa-sparkles" style="color:var(--gold-primary);"></i> ${text}`;
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

    console.log("✨ ComeTripWithMe 3-Tier Travel Segment Engine (Luxury · Mid-Tier · Budget) loaded.");
});
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated 3-tier index.html with {len(html_template)} characters.")
