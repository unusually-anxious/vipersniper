"use client"

import useSWR from "swr"
import { getZeroBid } from "@/lib/api"

export default function Dashboard() {
  const { data } = useSWR("zeroBid", getZeroBid)

  if (!data) return <div>Loading...</div>

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold">
        Dashboard
      </h1>
      <p>
        {data.length} zero bid opportunities
      </p>
    </div>
  )
}
