import React, { useState } from 'react'
import './App.css'
import ListingPage from './ListingPage'

function App() {
  const [toggleHotel, setToggleHotel] = useState(false)

  const mockListings = [
    {
      listing: {
        id: 1,
        communityId: 1,
        listedById: 1,
        createdOn: new Date("2024-03-22"),
        listedOn: new Date("2024-03-22"),
        closedOn: null,
        status: "active",
        listingType: "item",
        saleType: "sell",
        priceCents: 12999,
        title: 'Stylish Sneakers',
        description: 'The perfect shoe for the stylish athlete.',
      },
      item: {
        id: 1,
        itemName: "Used Air Jordans",
        condition: "acceptable",
        photos: [
          {
            caption: "side view",
            url: "https://www.crepslocker.com/cdn/shop/files/air-jordan-4-retro-red-cement-_2023_-dh6927-161-side.jpg?width=300",
          },
          {
            caption: "front view",
            url: "https://www.crepslocker.com/cdn/shop/files/air-jordan-4-retro-red-cement-_2023_-dh6927-161-front-side.jpg?width=300",
          },
        ],
        shipping_zipcode: 94115,
        itemDetails: {
          "yearOfProduction": 2021,
          "sneakerwebReference": "https://sneakerweb.com/sneakers/air-jordan-432/",
          "shoeSize": 12,
        },
      },
      sourceItem: {
        sourceItemName: "Air Jordan, Retro 4",
        sourceCategoryId: 43,
        sourceItemDetails: {
          brand: "Nike",
          model: "Air Jordan",
          style: "Retro 4",
          color: "red/cement",
          originalPrice: 109.99,
          firstProduced: 2020,
        }
      },
    },
    {
      listing: {
        id: 2,
        communityId: 1,
        listedById: 1,
        createdOn: new Date("2024-03-22"),
        listedOn: new Date("2024-03-22"),
        closedOn: null,
        status: "active",
        listingType: "lodging",
        saleType: "book",
        priceCents: 15099,
        title: 'Studio (garden view)',
        description: 'Our standard 650 ft. studio with kitchenette.',
      },
      lodging: {
        lodgingName: "Hilton - Downtown Indianapolis",
        address: "123 Main St., Indianapolis, IN 12345",
        startDate: new Date("2024-05-01"),
        endDate: new Date("2024-05-03"),
        lodgingType: "hotel",
        lodgingUrl: "https://hilton.com/indy/",
        lodgingDetails: {
          discount: "10% conference discount for community members",
          totalRoomsInBlock: 30,
          availableRooms: 14,
        },
      },
    }
  ]

  return (
    <div className="App">
      <div className="mb-4">
        <input
          type="checkbox"
          id="toggle-hotel"
          checked={toggleHotel}
          onChange={() => setToggleHotel(!toggleHotel)}
        />
        <div className="d-inline-block p-2">
          <label className="mr-2" htmlFor="toggle-hotel">
            Toggle Hotel Listing?
          </label>
        </div>
      </div>
      <ListingPage listing={mockListings[toggleHotel ? 1 : 0]} />
    </div>
  )
}

export default App
