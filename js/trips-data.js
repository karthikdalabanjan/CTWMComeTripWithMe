// ComeTripWithMe Curated Dataset

const TRIP_VIBES = {
  PARTY: { label: "Party", emoji: "🎉", color: "#DC503C" },
  BACKPACKING: { label: "Backpacking", emoji: "🎒", color: "#4B5563" },
  CHILL: { label: "Chill & Slow", emoji: "🏔️", color: "#3CA082" },
  LUXURY: { label: "Luxury Escapes", emoji: "✨", color: "#E8C97A" },
  HERITAGE: { label: "Ancient Heritage", emoji: "🏛️", color: "#B37D4E" }
};

const CURATED_TRIPS = [
  {
    id: "goa",
    name: "Goa",
    headline: "Beach days, cliffside sundowners, zero tourist traps.",
    description: "Forget the crowded commercial packages. We hit the real North Goa secret spots, cliff viewpoints, legendary bakeries, and wind down with tranquil South Goa kayaking.",
    vibe: "PARTY",
    duration: "4D / 3N",
    price: "₹8,999",
    budgetValue: 8999,
    imageUrl: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=1000&q=80",
    heroTags: ["Sunset Views", "Secret Shacks", "Scooter Crawl", "South Coast Kayak"],
    totalEstimateDetails: "₹8,999 / person (Stays, scooty rental, boat kayak & curated entry)",
    creatorNote: "Goa is only as good as the spots you know. Skip the generic Calangute madness. Follow this day-by-day map.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "North Goa Landing & Sundowner",
        summary: "Land, pick up rented scooters, check into beachside villa, and catch golden hour at Anjuna cliff.",
        stops: [
          {
            id: "goa_d1_s1",
            name: "Anjuna Cliff & Curlies Trail",
            timing: "4:30 PM",
            category: "Sunset Viewpoint",
            description: "Rocky beach edge where psychedelic Goa culture began. Great music and raw ocean energy.",
            insiderTip: "Arrive 45 mins before sunset to grab the top deck corner table facing the rocks.",
            photoUrl: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80",
            lat: 15.5804,
            lng: 73.7431,
            audioStory: {
              title: "The True Story of Anjuna & The 70s Hippie Trail",
              durationSeconds: 110,
              narrator: "ComeTripWithMe Creator",
              scriptText: "You're standing on the iconic red laterite cliffs of Anjuna. In the late 1960s, world travelers arrived here on old Enfield motorcycles from Europe. Notice the volcanic rocks below. When the tide hits them right around 5:30 PM, the sea spray catches the sunset in brilliant gold."
            }
          },
          {
            id: "goa_d1_s2",
            name: "Anjuna Night Flea Market",
            timing: "8:00 PM",
            category: "Night Market",
            description: "Handmade leather, live acoustic bands, Goan sausages, and chilled draught beer.",
            insiderTip: "Bargain with a smile. The spice stalls at the back have authentic homemade peri-peri masala.",
            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
            lat: 15.5780,
            lng: 73.7410
          }
        ],
        foodSpots: [
          {
            name: "Curlies Shack",
            specialty: "Woodfired pizza & Kingfish Rava fry",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Crispy Kingfish Rava Fry with lemon butter",
            approxCostForTwo: "₹800 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Crispy Kingfish Rava fry right by Anjuna rocks 🌊",
            reelViews: "54K views 🎥"
          },
          {
            name: "Infantaria Pastry",
            specialty: "Authentic Goan breakfast & bebinca",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Goan Sausage Poee & Bebinca",
            approxCostForTwo: "₹450 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Flaky Goan Poee & fresh Bebinca morning crawl 🥐",
            reelViews: "38K views 🎥"
          }
        ],
        creatorSecretTip: "Rent your scooter right outside the airport or Thivim station — never through hotel front desks who charge 2x markup."
      },
      {
        dayNumber: 2,
        title: "North Goa Deep Dive & Fort Viewpoints",
        summary: "Sunrise walk at Chapora, breakfast at a French bakery, and sunset cliff vibes at Vagator.",
        stops: [
          {
            id: "goa_d2_s1",
            name: "Chapora Fort Vista",
            timing: "8:00 AM",
            category: "Heritage Fort",
            description: "The famous Dil Chahta Hai rampart overlooking the Chapora River meeting the Arabian Sea.",
            insiderTip: "Climb the northern bastion wall for an unobstructed view of Morjim sandbar.",
            photoUrl: "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=600&q=80",
            lat: 15.6059,
            lng: 73.7380,
            audioStory: {
              title: "Chapora Fort: Portuguese Cannons & Bollywood Lore",
              durationSeconds: 125,
              narrator: "ComeTripWithMe Creator",
              scriptText: "Built in 1717 by the Portuguese over older Adil Shahi ruins, Chapora was designed to defend against Maratha raids. Look out across the river mouth toward Morjim — that sand spit is where endangered Olive Ridley turtles nest in winter."
            }
          },
          {
            id: "goa_d2_s2",
            name: "Little Vagator Hidden Cove",
            timing: "3:30 PM",
            category: "Secret Beach",
            description: "Carved rock faces, Shiva face rock carving, and dramatic red cliffs.",
            insiderTip: "Walk past the main entrance stairs toward the southern cliff path to skip the crowd.",
            photoUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
            lat: 15.5980,
            lng: 73.7390
          }
        ],
        foodSpots: [
          {
            name: "Thalassa Greek Taverna",
            specialty: "Greek cuisine & sunset cocktail",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Souvlaki wraps & Baklava",
            approxCostForTwo: "₹1,800 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Sunset dining vibes & souvlaki platter at Thalassa 🌅",
            reelViews: "82K views 🎥"
          },
          {
            name: "Mango Tree Bar",
            specialty: "Late-night Goan curry & cold beer",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Prawns Balchão with Steamed Rice",
            approxCostForTwo: "₹700 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Spicy Goan Prawn Balchão served with steaming rice 🦐",
            reelViews: "29K views 🎥"
          }
        ],
        creatorSecretTip: "Book Thalassa sunset table at least 3 days in advance via their Instagram DM or WhatsApp."
      },
      {
        dayNumber: 3,
        title: "South Goa Tranquil Switch & Kayaking",
        summary: "Drive down through old Portuguese village lanes to Palolem's crescent bay and secret butterfly cove.",
        stops: [
          {
            id: "goa_d3_s1",
            name: "Palolem Crescent Beach",
            timing: "11:00 AM",
            category: "Calm Beach",
            description: "Gentle bay framed by lush coconut groves, colorful wooden shacks, and dolphins.",
            insiderTip: "Rent a single kayak for ₹300/hr and paddle around Canacona Island on the north end.",
            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
            lat: 15.0100,
            lng: 74.0231,
            audioStory: {
              title: "Palolem: The Secret Dolphin Sanctuary",
              durationSeconds: 95,
              narrator: "ComeTripWithMe Creator",
              scriptText: "Notice how calm the water is here compared to North Goa? Palolem is a natural amphitheater of granite headlands. If you kayak out 300 meters early morning, Indo-Pacific humpback dolphins frequently surface right next to your boat."
            }
          },
          {
            id: "goa_d3_s2",
            name: "Butterfly Beach Sunset Boat",
            timing: "4:45 PM",
            category: "Hidden Lagoon",
            description: "Secluded cove surrounded by dense jungle, only reachable by boat or jungle trek.",
            insiderTip: "Take the 15-minute boat from Palolem right around 4:30 PM to catch sunset without getting stranded after dark.",
            photoUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&q=80",
            lat: 15.0250,
            lng: 74.0090
          }
        ],
        foodSpots: [
          {
            name: "Dropadi Beach Restaurant",
            specialty: "Fresh catch of the day on Palolem beach",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Butter Garlic Squid & Coconut Rice",
            approxCostForTwo: "₹950 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Butter Garlic Squid cooked fresh on Palolem sands 🦑",
            reelViews: "44K views 🎥"
          }
        ],
        creatorSecretTip: "Ask the fishermen at Palolem south end for a shared boat ride to Butterfly Beach — it's ₹400 per person instead of ₹1800 private."
      },
      {
        dayNumber: 4,
        title: "Arambol Morning & Flight Out",
        summary: "Fresh ocean swim, sweet lake drum circle memories, artisan bakery breakfast, and return flight.",
        stops: [
          {
            id: "goa_d4_s1",
            name: "Arambol Sweet Water Lake",
            timing: "7:30 AM",
            category: "Freshwater Lagoon",
            description: "Natural freshwater lagoon sitting 50 meters away from the crashing ocean waves.",
            insiderTip: "Dip in the lake first, then walk up the jungle path to see the ancient Banyan tree.",
            photoUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
            lat: 15.6880,
            lng: 73.7020
          }
        ],
        foodSpots: [
          {
            name: "Baba Au Rhum",
            specialty: "Acclaimed wood-fired French bakery",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Ham & Cheese Croissant + Filter Coffee",
            approxCostForTwo: "₹650 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Croissants and woodfired sourdough breakfast reel 🥐",
            reelViews: "61K views 🎥"
          }
        ],
        creatorSecretTip: "Pick up Goan cashew feni and spiced choriz sausages from Mapusa Market on the way to the airport."
      }
    ]
  },
  {
    id: "thailand",
    name: "Thailand",
    headline: "Street food at midnight. Emerald islands at sunrise.",
    description: "7 days across electric Bangkok street food alleyways and the dramatic limestone sea cliffs of Krabi. We bypass overpriced tours and show you the exact local ferries and food carts.",
    vibe: "BACKPACKING",
    duration: "7D / 6N",
    price: "₹34,999",
    budgetValue: 34999,
    imageUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=1000&q=80",
    heroTags: ["Bangkok Street Food", "Wat Arun Sunrise", "Phi Phi Islands", "Krabi Cliffs"],
    totalEstimateDetails: "₹34,999 / person (Hostels/Boutique stays, domestic flights, ferries & food crawl)",
    creatorNote: "Thailand is ruined by bad itineraries. Our route ensures you eat like a Bangkok local and see Maya Bay before the tourist speedboats arrive.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "Bangkok Arrival & Khao San Night Walk",
        summary: "Land in Suvarnabhumi, take the Airport Rail Link, eat spicy holy basil chicken, and explore old city alleyways.",
        stops: [
          {
            id: "th_d1_s1",
            name: "Khao San & Rambuttri Road",
            timing: "8:00 PM",
            category: "Backpacker Hub",
            description: "The heartbeat of Southeast Asian backpacking, street artists, and fried noodle stalls.",
            insiderTip: "Skip noisy Khao San main street; walk one block north to Soi Rambuttri for better vibes.",
            photoUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&q=80",
            lat: 13.7588,
            lng: 100.4975,
            audioStory: {
              title: "Khao San Road: The Accidental Backpacker Capital",
              durationSeconds: 105,
              narrator: "ComeTripWithMe Creator",
              scriptText: "Until 1982, Khao San was just a quiet rice market street in Bangkok. When Thailand celebrated its Bangkok bicentennial, travelers looking for cheap lodging knocked on local family doors here. Today it's the global backpacker rite of passage."
            }
          }
        ],
        foodSpots: [
          {
            name: "Thip Samai Pad Thai",
            specialty: "World-renowned egg-wrapped Pad Thai",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Superb Pad Thai with fresh prawns & orange juice",
            approxCostForTwo: "400 THB for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1559847844-5315695dadae?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Watch the legendary egg-wrapped Pad Thai flame wok show 🔥",
            reelViews: "96K views 🎥"
          }
        ],
        creatorSecretTip: "Exchange currency at SuperRich counters in Suvarnabhumi Airport basement for the highest rate in Thailand."
      },
      {
        dayNumber: 2,
        title: "Wat Arun Sunrise & Riverside Markets",
        summary: "Watch early golden light hit the porcelain spires of Temple of Dawn, take the 5-baht river ferry, and explore Chinatown food stalls.",
        stops: [
          {
            id: "th_d2_s1",
            name: "Wat Arun (Temple of Dawn)",
            timing: "7:30 AM",
            category: "Ancient Temple",
            description: "Majestic spire covered in thousands of colorful glazed Chinese porcelain mosaics along Chao Phraya.",
            insiderTip: "Rent traditional Thai attire at the temple gate for ₹200 for iconic photography.",
            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
            lat: 13.7437,
            lng: 100.4889,
            audioStory: {
              title: "Wat Arun: The Porcelain Temple by the River of Kings",
              durationSeconds: 120,
              narrator: "ComeTripWithMe Creator",
              scriptText: "Wat Arun stands 82 meters high on the west bank of the Chao Phraya River. Notice the porcelain tiles? In the 18th century, Chinese merchant ships used broken porcelain plates as ballast weights to balance their ships — King Rama III used those discarded plates to decorate this entire temple."
            }
          },
          {
            id: "th_d2_s2",
            name: "Yaowarat Chinatown Food Mile",
            timing: "7:00 PM",
            category: "Food Market",
            description: "Neon signs, sizzling woks, crab fried rice, and mango sticky rice carts.",
            insiderTip: "Look for the green Michelin Bib Gourmand plaques on humble cart wheels.",
            photoUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
            lat: 13.7408,
            lng: 100.5108
          }
        ],
        foodSpots: [
          {
            name: "Guay Tiew Kua Gai",
            specialty: "Michelin rated wok-fried chicken flat noodles",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Smoky roasted chicken rice noodles with soft egg",
            approxCostForTwo: "150 THB for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Michelin Bib Gourmand smoky wok flat noodles 🥢",
            reelViews: "88K views 🎥"
          }
        ],
        creatorSecretTip: "Use the Chao Phraya Express Orange Flag boat for 16 THB to travel anywhere along the river instead of tourist boats."
      },
      {
        dayNumber: 3,
        title: "Fly to Krabi & Railay Beach Sunset",
        summary: "Morning 1-hour flight to Krabi, check into beach hotel, longtail boat to Railay surrounded by limestone towers.",
        stops: [
          {
            id: "th_d3_s1",
            name: "Railay Beach & Phra Nang Cave",
            timing: "3:30 PM",
            category: "Limestone Peninsula",
            description: "Cut off from the mainland by gigantic karst cliffs, accessible exclusively by wooden longtail boat.",
            insiderTip: "Walk from Railay West to Railay East at low tide to watch rock climbers scale 150m vertical cliffs.",
            photoUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
            lat: 8.0119,
            lng: 98.8396,
            audioStory: {
              title: "Railay: The Fortress Cut Off by Ancient Cliffs",
              durationSeconds: 110,
              narrator: "ComeTripWithMe Creator",
              scriptText: "Because towering limestone headlands block all roads from the mainland, Railay has zero cars and zero scooters. You arrive by splashing into the turquoise surf from a wooden longtail boat. It feels like entering an untouched island paradise."
            }
          }
        ],
        foodSpots: [
          {
            name: "Krabi Town Night Market",
            specialty: "Southern Thai curries & roti stalls",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Banana Nutella Roti + Green Curry",
            approxCostForTwo: "300 THB for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Hot Banana Nutella Roti cooked live in Krabi 🥞",
            reelViews: "52K views 🎥"
          }
        ],
        creatorSecretTip: "Book longtail boat tickets directly at the Ao Nang cooperative booth at the beach head for fixed standard rates."
      },
      {
        dayNumber: 4,
        title: "Early Bird Phi Phi & Maya Bay Run",
        summary: "6:30 AM speedboat to Maya Bay before the 10:00 AM tourist crowds arrive from Phuket.",
        stops: [
          {
            id: "th_d4_s1",
            name: "Maya Bay & Pileh Lagoon",
            timing: "7:45 AM",
            category: "World Heritage Bay",
            description: "Dramatic 100-meter cliffs enclosing crystalline emerald water and blacktip reef sharks.",
            insiderTip: "Swim inside Pileh Lagoon where the water is calm like a heated swimming pool.",
            photoUrl: "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=600&q=80",
            lat: 7.6784,
            lng: 98.7672
          }
        ],
        foodSpots: [
          {
            name: "Island Boat Fresh Catch",
            specialty: "Barbecue seafood cooked fresh on longtail boat",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Grilled Tiger Prawns & Papaya Salad",
            approxCostForTwo: "500 THB for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Freshly grilled tiger prawns right on the island beach 🦐",
            reelViews: "68K views 🎥"
          }
        ],
        creatorSecretTip: "Take an early 6:30 AM departure. You'll have Maya Bay almost entirely to yourself for pristine photos."
      }
    ]
  },
  {
    id: "himachal",
    name: "Himachal Pradesh",
    headline: "The mountains will fix whatever is broken in you.",
    description: "Riverside Kasol cafés, Kheerganga hot springs trek, Solang snow peaks, and serene pine forest walks. Authentic homestays and zero commercial tourist jams.",
    vibe: "CHILL",
    duration: "6D / 5N",
    price: "₹12,999",
    budgetValue: 12999,
    imageUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=1000&q=80",
    heroTags: ["Kheerganga Hot Springs", "Old Manali Cafés", "Beas River Walks", "Mountain Homestays"],
    totalEstimateDetails: "₹12,999 / person (Volvo transit, valley homestays, trek guides & hot meals)",
    creatorNote: "Himachal changes you. The secret is knowing which village to sleep in so you hear the pine needles, not car honks.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "Delhi/Chandigarh Volvo to Kasol",
        summary: "Scenic overnight bus ascending into the Parvati Valley. Wake up to misty river views and fresh ginger lemon honey tea.",
        stops: [
          {
            id: "hp_d1_s1",
            name: "Parvati River Bank Walk",
            timing: "9:00 AM",
            category: "Riverside Nature",
            description: "Glacial turquoise waters roaring through giant mossy granite boulders and pine woods.",
            insiderTip: "Cross the suspension bridge toward Chalal village for secluded wooden riverside benches.",
            photoUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=600&q=80",
            lat: 32.0098,
            lng: 77.3150,
            audioStory: {
              title: "Parvati Valley: The Legend of Shiva's Meditation",
              durationSeconds: 100,
              narrator: "ComeTripWithMe Creator",
              scriptText: "According to folklore, Lord Shiva meditated here in this valley for three thousand years. As you listen to the roaring Parvati River, you'll understand why travelers from across the world come here to disconnect."
            }
          }
        ],
        foodSpots: [
          {
            name: "Café 1947",
            specialty: "Old Manali's oldest Italian riverside café",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Woodfired Quattro Formaggi & Hot Chocolate",
            approxCostForTwo: "₹850 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Riverside woodfired pizza listening to roaring Beas river 🍕",
            reelViews: "59K views 🎥"
          }
        ],
        creatorSecretTip: "Carry cash in Kasol and Parvati valley. ATMs frequently run dry in peak mountain season."
      },
      {
        dayNumber: 2,
        title: "The Kheerganga Trek & Natural Hot Springs",
        summary: "12km trek through apple orchards, pine forests, and waterfalls to natural sulfur hot springs under the stars.",
        stops: [
          {
            id: "hp_d2_s1",
            name: "Kheerganga Hot Spring Top",
            timing: "3:30 PM",
            category: "Natural Hot Spring",
            description: "Natural therapeutic hot sulfur pool overlooking snowcapped 4,000m Himalayan ridges.",
            insiderTip: "Enter the pool right around sunset when the mountain air chills to 8°C — pure magic.",
            photoUrl: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80",
            lat: 31.9890,
            lng: 77.5020
          }
        ],
        foodSpots: [
          {
            name: "Dylan's Toasted & Roasted",
            specialty: "Iconic coffee and cookie corner",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Warm Chocolate Chip Cookie with Espresso",
            approxCostForTwo: "₹300 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Old Manali's iconic hot chocolate chip cookie & espresso ☕",
            reelViews: "43K views 🎥"
          }
        ],
        creatorSecretTip: "Start the trek from Barshaini by 8:30 AM to reach the top comfortably before afternoon mist rolls in."
      }
    ]
  },
  {
    id: "pondicherry",
    name: "Pondicherry",
    headline: "French heritage lanes, Indian soul, ₹400 filter coffee & croissants.",
    description: "Cycle through the mustard-yellow French Quarter at 6:30 AM before tourists wake up. Experience spiritual Auroville, golden beaches, and authentic French bakeries.",
    vibe: "CHILL",
    duration: "3D / 2N",
    price: "₹4,999",
    budgetValue: 4999,
    imageUrl: "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=1000&q=80",
    heroTags: ["White Town French Quarter", "Auroville Matrimandir", "Promenade Sunrise", "Artisanal Bakeries"],
    totalEstimateDetails: "₹4,999 / person (Heritage stay, vintage cycle rental, Auroville entry & café trail)",
    creatorNote: "Pondi is meant to be done slowly. Wake up at 6:00 AM, rent a cycle with a wicker basket, and smell the fresh baguettes.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "White Town Heritage Walk & Promenade",
        summary: "French Quarter architecture, bougainvillea covered colonial gates, and ocean breeze.",
        stops: [
          {
            id: "pon_d1_s1",
            name: "White Town French Quarter",
            timing: "6:30 AM",
            category: "Heritage Architecture",
            description: "Preserved 18th-century French colonial mansions, arched windows, and cobblestone lanes.",
            insiderTip: "Rue Suffren and Rue Romain Rolland have the most vibrant yellow colonial façades.",
            photoUrl: "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&q=80",
            lat: 11.9338,
            lng: 79.8350,
            audioStory: {
              title: "White Town: Where France Met the Coromandel Coast",
              durationSeconds: 115,
              narrator: "ComeTripWithMe Creator",
              scriptText: "In 1674, the French East India Company designed this grid city with a canal separating the French Quarter from the Tamil Quarter. As you cycle past these arched doorways, notice how Tamil courtyard architecture blended into French balconies."
            }
          }
        ],
        foodSpots: [
          {
            name: "Baker Street",
            specialty: "French boulangerie and viennoiseries",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Almond Croissant & Quiche Lorraine",
            approxCostForTwo: "₹450 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Flaky Parisian almond croissants in French Quarter 🥐",
            reelViews: "64K views 🎥"
          }
        ],
        creatorSecretTip: "Rent a classic bicycle near the railway station for ₹100/day rather than booking expensive e-rickshaws."
      }
    ]
  },
  {
    id: "malaysia",
    name: "Malaysia",
    headline: "KL skyline to Penang street food legacy in 4 hours.",
    description: "5 days taking you from the gleaming Petronas Towers and Batu Caves to the UNESCO World Heritage street murals and sizzling hawker stalls of George Town.",
    vibe: "BACKPACKING",
    duration: "5D / 4N",
    price: "₹24,999",
    budgetValue: 24999,
    imageUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=1000&q=80",
    heroTags: ["Petronas Towers", "George Town UNESCO", "Jalan Alor Night Market", "Penang Food Trail"],
    totalEstimateDetails: "₹24,999 / person (Boutique hotels, KTM ETS express train, city transfers & food tour)",
    creatorNote: "Penang has the best street food on planet Earth. This trip is designed completely around your palate.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "Kuala Lumpur Neon & Batu Caves",
        summary: "Climb the 272 rainbow steps at Batu Caves and experience the night glow of Petronas Twin Towers.",
        stops: [
          {
            id: "my_d1_s1",
            name: "Batu Caves Rainbow Steps",
            timing: "8:00 AM",
            category: "Limestone Shrine",
            description: "Gigantic 140-foot golden Lord Murugan statue guarding 400-million-year-old limestone cavern.",
            insiderTip: "Beware of macaque monkeys; do not carry plastic bags or uncovered snacks on the stairs.",
            photoUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
            lat: 3.2379,
            lng: 101.6840
          }
        ],
        foodSpots: [
          {
            name: "Jalan Alor Night Market",
            specialty: "Sizzling street food central",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Satay Skewers with peanut sauce & Char Kway Teow",
            approxCostForTwo: "45 MYR for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Char Kway Teow wok hei & sizzling peanut chicken satay 🍢",
            reelViews: "77K views 🎥"
          }
        ],
        creatorSecretTip: "Take the KTM ETS high-speed train from KL Sentral to Butterworth (Penang) — comfortable 4-hour scenic ride."
      }
    ]
  },
  {
    id: "krabi",
    name: "Krabi",
    headline: "The kind of turquoise water that breaks your camera settings.",
    description: "5 days in paradise. Railay peninsula cliffs, 4 Islands longtail cruise, emerald freshwater lagoons, and sunset beach seafood barbecues.",
    vibe: "LUXURY",
    duration: "5D / 4N",
    price: "₹28,999",
    budgetValue: 28999,
    imageUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1000&q=80",
    heroTags: ["Railay Beach", "4-Islands Cruise", "Tiger Cave Vista", "Emerald Pool"],
    totalEstimateDetails: "₹28,999 / person (Resort stay, private longtail charter, kayak rentals & meals)",
    creatorNote: "Krabi feels completely different from commercial Phuket. More jungle, higher cliffs, and untouched emerald coves.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "Arrive Krabi & Ao Nang Beach Sunset",
        summary: "Fly directly into Krabi Airport. Check into oceanfront resort and watch longtail boats silhouetted against the sunset.",
        stops: [
          {
            id: "kb_d1_s1",
            name: "Noppharat Thara Sunset Strip",
            timing: "5:30 PM",
            category: "Sunset Beach",
            description: "Lush pine-fringed coastline with sand flats extending out to offshore islands during low tide.",
            insiderTip: "Walk across the shallow sand spit to Koh Khao Sam Hak during low tide at 5:00 PM.",
            photoUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
            lat: 8.0410,
            lng: 98.8100
          }
        ],
        foodSpots: [
          {
            name: "The Hilltop Restaurant",
            specialty: "Panoramic cliff dining over Ao Nang bay",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Steamed Seabass with lime and garlic",
            approxCostForTwo: "850 THB for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Seabass with fresh lime & garlic overlooking the sunset cliffs 🐟",
            reelViews: "58K views 🎥"
          }
        ],
        creatorSecretTip: "Fly straight into KBV (Krabi Airport) rather than landing in Phuket and enduring a 3.5 hour road transfer."
      }
    ]
  },
  {
    id: "gokarna",
    name: "Gokarna",
    headline: "Cliff hikes, hidden crescent coves, and acoustic campfire nights.",
    description: "4 days discovering the raw beauty of coastal Karnataka. The 5-beach cliff trek, Half Moon beach camp, secret lagoons, and oceanfront shacks.",
    vibe: "CHILL",
    duration: "4D / 3N",
    price: "₹4,499",
    budgetValue: 4499,
    imageUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1000&q=80",
    heroTags: ["5-Beach Cliff Trek", "Om Beach Rock Formations", "Half Moon Seclusion", "Kudle Sunset"],
    totalEstimateDetails: "₹4,499 / person (Beach huts, cliff guide, ferry transfers & fresh seafood)",
    creatorNote: "Gokarna is what Goa was 30 years ago. Pure nature, zero chaos, and breathtaking cliffside paths.",
    youtubeVideoId: "Cometripwithme",
    days: [
      {
        dayNumber: 1,
        title: "Kudle Beach & Sunset Drum Circle",
        summary: "Check into cliff hut above Kudle Beach, fresh coconut water, and sunset over the Arabian Sea.",
        stops: [
          {
            id: "gk_d1_s1",
            name: "Kudle Beach Cliff Path",
            timing: "4:00 PM",
            category: "Scenic Cliff",
            description: "Winding coastal cliff trail connecting Gokarna town to Kudle's sweeping sandy bay.",
            insiderTip: "Wear proper sneakers for the rocky cliff walk down to the beach.",
            photoUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
            lat: 14.5300,
            lng: 74.3160
          }
        ],
        foodSpots: [
          {
            name: "Namaste Café Om Beach",
            specialty: "Iconic seaside terrace eatery",
            recommendedBy: "@beyondbengalurufoods",
            mustTryDish: "Nutella Banana Pancake & Iced Lemon Tea",
            approxCostForTwo: "₹400 for two",
            reelThumbnailUrl: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
            reelUrl: "https://www.instagram.com/beyondbengalurufoods/",
            reelCaption: "Nutella banana pancakes right on the rock ledge of Om Beach 🥞",
            reelViews: "42K views 🎥"
          }
        ],
        creatorSecretTip: "Start the 5-beach trek (Kudle -> Om -> Half Moon -> Paradise -> God's Own) early at 6:30 AM."
      }
    ]
  }
];

const SPOTLIGHTS = [
  {
    id: "bengaluru",
    title: "Bengaluru & Beyond",
    subtitle: "Urban culture, heritage lanes & secret dosas",
    region: "Karnataka · Urban Culture",
    documentedSpotsCount: "15+ documented spots",
    imageUrl: "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=800&q=80",
    tags: ["Food Walks", "Malleswaram Heritage", "Cubbon Park", "Secret Filter Coffee"],
    overview: "Bengaluru isn't just tech corridors and traffic. The real city lives in 80-year-old Malleswaram darshinis, shady Cubbon canopy trails, old cantonment bakeries, and sunrise climbs up Skandagiri.",
    bestSeason: "All Year Round (Best: Oct – Feb)",
    durationRec: "2 - 3 Days Weekend Trail",
    documentedSpots: [
      {
        name: "CTR (Central Tiffin Room), Malleswaram",
        category: "Iconic Breakfast",
        tip: "Get the crispy Benne Masala Dosa with hot degree filter coffee before 9:30 AM."
      },
      {
        name: "Cubbon Park Bamboo Grove Trail",
        category: "Nature Walk",
        tip: "Sunday mornings 6–8 AM are vehicle-free. Perfect for cycling, dog walks and acoustic jams."
      },
      {
        name: "Brahmin's Coffee Bar, Shankarapura",
        category: "Heritage Dosa & Idli",
        tip: "Dip piping hot button idlis and crisp uddina vade directly into unlimited slow-churned coconut chutney."
      },
      {
        name: "Malleswaram 8th Cross Flower & Spice Market",
        category: "Street Photography",
        tip: "Visit at 6:30 AM when fresh jasmine strings, temple spices, and street vendors set up."
      },
      {
        name: "Skandagiri Sunrise Night Trek",
        category: "Adventure Ridge Trek",
        tip: "Book the Karnataka Eco-Tourism permit online 3 days in advance. Summit above the morning cloud layer."
      }
    ],
    foodHighlights: ["Crispy Butter Benne Dosa", "Degree Filter Coffee", "Khara Bath & Kesari Bath", "Mangalore Buns", "Saffron Halwa"],
    creatorAdvice: "Skip the generic commercial weekend pubs. Do a 6:00 AM breakfast crawl across Basavanagudi and Malleswaram instead."
  },
  {
    id: "coorg",
    title: "Coorg & Chikmagalur",
    subtitle: "Coffee estates, misty mountain sunrises & waterfalls",
    region: "Western Ghats · Hill Stations",
    documentedSpotsCount: "12+ verified trails",
    imageUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
    tags: ["Coffee Plantations", "Mullayanagiri Peak", "Abbi Falls", "Homestay Dinners"],
    overview: "The coffee heartland of India. Endless rolling emerald hills, estate homestays where you wake up to birdsong and freshly roasted Arabica, and misty 4x4 jeep trails cutting through tea ridges.",
    bestSeason: "September to March (Monsoons for waterfalls)",
    durationRec: "3 - 4 Days Getaway",
    documentedSpots: [
      {
        name: "Mullayanagiri Peak Sunrise Point",
        category: "Highest Peak in Karnataka",
        tip: "Reach the base by 5:30 AM to climb the 500 steps and watch the sea of morning clouds below."
      },
      {
        name: "Private Coffee Plantation Walk",
        category: "Estate Experience",
        tip: "Book a homestay inside an active plantation for direct bean-to-cup brewing and pepper vine walks."
      },
      {
        name: "Abbi Falls Hidden Stream Trail",
        category: "Waterfall Trail",
        tip: "Walk 200 meters downstream past the crowded main viewing deck for secluded natural rock pools."
      },
      {
        name: "Mandalpatti 4x4 Jeep Ridge Trail",
        category: "Off-Road Viewpoint",
        tip: "Hire an open 4x4 Mahindra Thar from Madikeri town for the exhilarating golden-hour ridge ride."
      },
      {
        name: "Namdroling Golden Temple, Bylakuppe",
        category: "Tibetan Monastic Culture",
        tip: "Attend the 1:00 PM prayer chant inside the grand temple hall and grab handmade steamed momos in the settlement."
      }
    ],
    foodHighlights: ["Authentic Pandi Curry with Akki Roti", "Coorg Wild Forest Honey", "Estate Roasted Filter Coffee", "Bamboo Shoot Curry (Baimbale)"],
    creatorAdvice: "Never book generic town hotels in central Madikeri. Pick a verified estate homestay at least 15 km out in the hills."
  },
  {
    id: "hampi",
    title: "Hampi & Badami Ruins",
    subtitle: "Boulders, Vijayanagara empire & Tungabhadra sunsets",
    region: "Ancient · UNESCO World Heritage",
    documentedSpotsCount: "18+ historical spots",
    imageUrl: "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?w=800&q=80",
    tags: ["Virupaksha Temple", "Matanga Hill", "Coracle Boat", "Hippie Island"],
    overview: "A surreal open-air museum of giant red granite boulders, ruined 14th-century palaces, sacred river ghats, and acoustic café vibes across the Tungabhadra river.",
    bestSeason: "October to March (Pleasant weather)",
    durationRec: "3 - 4 Days Circuit",
    documentedSpots: [
      {
        name: "Matanga Hill 360° Sunrise Point",
        category: "Epic Panoramic View",
        tip: "Start climbing 45 mins before sunrise with a flashlight from Achyutaraya temple side for the world's best boulder view."
      },
      {
        name: "Virupaksha Temple & Sacred Ghats",
        category: "Living 7th-Century Shrine",
        tip: "Catch Lakshmi the temple elephant during her morning river bath at 7:30 AM by the main ghat."
      },
      {
        name: "Coracle Boat Ride across Tungabhadra",
        category: "River Crossing",
        tip: "Hire a round woven coracle boat at dusk to glide past boulder canyons and ruined stone pavilions."
      },
      {
        name: "Hippie Island & Sanapur Lake Cliff Jump",
        category: "Chill Lagoon & Sunset",
        tip: "Rent a moped (₹300/day) and watch the sunset from Sanapur rocks with acoustic music."
      },
      {
        name: "Badami Cave Temples (6th Century CE)",
        category: "Rock-Cut Architecture",
        tip: "Cave 1 Nataraja carving is breathtaking in the soft morning eastern sunlight."
      }
    ],
    foodHighlights: ["South Indian Banana Leaf Thali at Mango Tree", "Falafel & Fresh Hummus Platters", "Fresh Sugarcane Lime Juice", "Woodfired Bouldering Pizzas"],
    creatorAdvice: "Stay on the Hampi Bazaar side for sunrise temple walks, or cross the river to Anegundi side for peaceful paddy field cottages."
  },
  {
    id: "thailand_spot",
    title: "Thailand & Islands",
    subtitle: "Bangkok street food woks & Krabi emerald lagoons",
    region: "Southeast Asia · Tropical",
    documentedSpotsCount: "24+ verified locations",
    imageUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
    tags: ["Railay Beach", "Wat Arun", "Maya Bay", "Yaowarat Chinatown"],
    overview: "The ultimate Southeast Asian run. High-octane Bangkok night markets and midnight tuk-tuks, followed by tranquil limestone karst cliff climbing in Krabi and Phi Phi lagoons.",
    bestSeason: "November to April (Dry & Sunny)",
    durationRec: "6 - 8 Days Circuit",
    documentedSpots: [
      {
        name: "Railay West to Phra Nang Beach",
        category: "Hidden Peninsula",
        tip: "Only reachable by longtail boat. Climb to the secret hidden lagoon at low tide through the jungle trail."
      },
      {
        name: "Yaowarat Chinatown Midnight Food Mile",
        category: "Culinary Mile",
        tip: "Look for the Michelin-starred Guay Tiew Kua Gai noodle wok cart in the narrow side alley."
      },
      {
        name: "Wat Arun (Temple of Dawn) River Pier",
        category: "Iconic Buddhist Prang",
        tip: "Take the 5-Baht cross-river ferry at 5:00 PM for stunning golden hour silhouette photos against Chao Phraya river."
      },
      {
        name: "Pileh Lagoon Emerald Swimming Basin",
        category: "Marine Sanctuary",
        tip: "Charter a private sunrise longtail boat from Phi Phi before the Phuket tour catamarans arrive at 10 AM."
      },
      {
        name: "Emerald Pool & Hot Springs, Krabi",
        category: "Jungle Thermal Bath",
        tip: "Go early morning around 8:00 AM when the natural jungle spring water is undisturbed and crystal clear."
      }
    ],
    foodHighlights: ["Pad Thai with Giant River Prawns", "Mango Sticky Rice with Coconut Cream", "Tom Yum Goong Seafood Soup", "Crispy Pork Belly Noodle Bowl"],
    creatorAdvice: "Exchange INR to THB at SuperRich booths in Bangkok airport basement level for 4% better rates than standard bank counters."
  }
];

const VIDEOS = [
  {
    id: "v1",
    title: "ComeTripWithMe: Real Trips, Real Proof (Watch Before You Book)",
    destination: "Bengaluru & Thailand",
    duration: "14:20",
    views: "45K views",
    thumbnailUrl: "https://images.unsplash.com/photo-1528181304800-259b08848526?w=800&q=80",
    videoUrl: "https://youtube.com/@Cometripwithme",
    highlights: ["Creator-Led Routes", "No tourist traps", "Real street prices", "Local contacts"]
  },
  {
    id: "v2",
    title: "Gokarna: The Secret Beach Nobody Tells You About",
    destination: "Gokarna Coast",
    duration: "9:45",
    views: "32K views",
    thumbnailUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    videoUrl: "https://youtube.com/@Cometripwithme",
    highlights: ["Half Moon cliff trail", "₹300 boat negotiation", "Hidden natural rock pool"]
  },
  {
    id: "v3",
    title: "Bengaluru Food Spots That Are Not On Any Online List",
    destination: "Bengaluru",
    duration: "11:15",
    views: "89K views",
    thumbnailUrl: "https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=800&q=80",
    videoUrl: "https://youtube.com/@Cometripwithme",
    highlights: ["Old City military hotel", "Crisp benne dosa", "₹20 filter coffee ritual"]
  },
  {
    id: "v4",
    title: "Himachal: The Riverside Mountain Café That Changed Everything",
    destination: "Parvati Valley",
    duration: "12:50",
    views: "58K views",
    thumbnailUrl: "https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80",
    videoUrl: "https://youtube.com/@Cometripwithme",
    highlights: ["Pine forest homestay", "Secret hot springs timing", "Trout fish preparation"]
  },
  {
    id: "v5",
    title: "KL to Penang in 4 Hours: The Malaysia Nobody Talks About",
    destination: "Malaysia",
    duration: "16:05",
    views: "27K views",
    thumbnailUrl: "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80",
    videoUrl: "https://youtube.com/@Cometripwithme",
    highlights: ["KTM train hack", "George Town Asam Laksa", "Murals without crowd"]
  }
];

const INSTAGRAM_POSTS = [
  {
    id: "ig1",
    handle: "@cometriipwme",
    channelType: "TRAVEL",
    caption: "The exact moment the morning sun broke over Chapora Fort. 0 tourists, 100% ocean breeze. 📍 Goa",
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
    caption: "Piping hot butter garlic kingfish rava fry right by the shore. The crunch is everything. 🍜",
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
  },
  {
    id: "ig5",
    handle: "@cometriipwme",
    channelType: "TRAVEL",
    caption: "Hiking the five beaches of Gokarna. Why pay ₹50,000 when this paradise is right in Karnataka? 🌊",
    location: "Om Beach, Gokarna",
    imageUrl: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&q=80",
    likesCount: "1,980"
  },
  {
    id: "ig6",
    handle: "@beyondbengalurufoods",
    channelType: "FOOD",
    caption: "The most comforting ginger lemon honey tea with apple strudel in Old Manali. ☕🏔️",
    location: "Old Manali, Himachal",
    imageUrl: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80",
    likesCount: "2,750"
  }
];

const TRAVELER_REVIEWS = [
  {
    id: "r1",
    authorHandle: "@rohini.explores",
    city: "Bengaluru",
    tripTag: "🌆 Old City Food Walk",
    rating: 5,
    reviewQuote: "Tried three different tour operators in Bengaluru. This was the only one that felt like an actual secret. The chai and military hotel spot alone was worth every rupee."
  },
  {
    id: "r2",
    authorHandle: "@arjun_wanders",
    city: "Chennai",
    tripTag: "☁️ Coorg & Chikmagalur Weekend",
    rating: 5,
    reviewQuote: "Watched the YouTube video, booked the trip, went. Every single stop matched the video proof. Felt like being inside a vlog in real life. That doesn't happen with agency brochures."
  },
  {
    id: "r3",
    authorHandle: "@priya.irl",
    city: "Hyderabad",
    tripTag: "🏔️ Himachal Mountain Trail",
    rating: 5,
    reviewQuote: "Finally a tour operator who communicates over WhatsApp like a normal human friend. Mullayanagiri and Kheerganga hit different. No PDF itinerary = 10/10."
  }
];

const DEFAULT_PACKING_LIST = [
  { id: "p1", title: "Valid Government ID & Booking confirmation", category: "Essentials", checked: true },
  { id: "p2", title: "Power bank (min 10,000 mAh)", category: "Tech", checked: false },
  { id: "p3", title: "Comfortable walking / trek shoes", category: "Apparel", checked: true },
  { id: "p4", title: "Sunscreen SPF 50+ & Sunglasses", category: "Care", checked: false },
  { id: "p5", title: "Quick-dry towel & Swimwear", category: "Apparel", checked: false },
  { id: "p6", title: "Offline downloaded map & music playlist", category: "Tech", checked: true }
];

function getSmartMatchRecommendation(destinationId, budget) {
  if (!destinationId) return null;
  switch (destinationId.toLowerCase()) {
    case "goa":
      if (budget && budget <= 5000) {
        return {
          title: "Goa Long Weekend — ₹4,999/person",
          sub: "3 nights North Goa. Budget beach shacks, scooty crawl, sunset at Curlies & Anjuna."
        };
      } else {
        return {
          title: "Full Goa Circuit — ₹8,999/person",
          sub: "4 nights, North + South Goa blend. Thalassa sunset, Chapora cliff views, and pristine Palolem silence."
        };
      }
    case "thailand":
      if (budget && budget <= 15000) {
        return {
          title: "Bangkok Budget Run — ₹12,999",
          sub: "7 nights, street food crawl, Wat Arun at sunrise, and hidden market alleys."
        };
      } else if (budget && budget <= 30000) {
        return {
          title: "Bangkok + Krabi Islands — ₹24,999",
          sub: "Best of both worlds: neon Bangkok nights & limestone cliff kayaking in Krabi."
        };
      } else {
        return {
          title: "Full Thailand Circuit — ₹34,999",
          sub: "Bangkok + Krabi + Phi Phi. 7 days with domestic transfers included."
        };
      }
    case "himachal":
      if (budget && budget <= 5000) {
        return {
          title: "Kasol & Kheerganga — ₹4,999",
          sub: "Bus from Delhi/Chd, 3 nights riverside homestay, hot springs & mountain café trail."
        };
      } else {
        return {
          title: "Manali + Spiti Edge — ₹12,999",
          sub: "6 nights. Old Manali base, trout fishing, Solang Valley, and high-altitude Buddhist passes."
        };
      }
    case "pondicherry":
      return {
        title: "Pondi French Coast — ₹4,999",
        sub: "3 nights. White Town heritage cycle walks, Auroville bakeries, and Serenity Beach sunrise."
      };
    case "malaysia":
      return {
        title: "KL + Penang Food Trail — ₹24,999",
        sub: "5 nights. Petronas night skyline to George Town street food legacy in 4 hours."
      };
    case "krabi":
      return {
        title: "Krabi Secret Lagoons — ₹28,999",
        sub: "5 nights. Railay Beach, 4-Islands longtail cruise, and emerald cave swimming."
      };
    case "gokarna":
      return {
        title: "Gokarna Slow Escape — ₹4,499",
        sub: "3 nights. Om Beach cliff trail, Half Moon cove trek, and beach campfire acoustic nights."
      };
    default:
      return {
        title: "Curated Creator Trip",
        sub: "Handpicked route verified with video proof. No tourist traps."
      };
  }
}
