export default function ListingCard({ listing }: any) {
  return (
    <div className="bg-[#1a2527] p-4 rounded-xl border border-[#355654]">
      <h3 className="text-lg font-semibold">{listing.title}</h3>
      <div className="text-sm text-gray-400">
        {listing.location} • Ends {listing.end_time}
      </div>
      <div className="flex justify-between mt-2">
        <span className="text-cyan-300 font-bold">
          ${listing.bid}
        </span>
        <span className="bg-purple-900 px-2 py-1 rounded">
          Score {listing.score}
        </span>
      </div>
    </div>
  )
}
