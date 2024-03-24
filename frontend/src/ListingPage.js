import React from 'react'
import ListingSection from './components/listingSection'
import ItemSection from './components/itemSection'
import SourceItemSection from './components/sourceItemSection'
import LodgingSection from './components/lodgingSection'

const ListingPage = (props) => {
  const { listing } = props

  return (
    <div>
      <ListingSection listing={listing.listing} />
      <ItemSection item={listing?.item} />
      <SourceItemSection sourceItem={listing?.sourceItem} />
      <LodgingSection lodging={listing?.lodging} />
    </div>
  )
}

export default ListingPage
