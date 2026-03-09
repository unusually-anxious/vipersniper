"use client"

import useSWR from "swr"
import { getListings } from "@/lib/api"
import ListingCard from "@/components/ListingCard"

export default function Hunter() {
  const { data } = useSWR("listings", getListings)

  if (!data) return <div>Loading...</div>

  return (
    <div className="p-6 grid gap-4">
      <h1 className="text-3xl font-bold">
        Zero-Bid Hunter
      </h1>

      <div className="grid md:grid-cols-3 gap-4">
        {data.map((listing: any) => (
          <ListingCard
            key={listing.id}
            listing={listing}
          />
        ))}
      </div>
    </div>
  )
}
