import axios from "axios"

export const api = axios.create({
  baseURL: "http://localhost:8000"
})

export async function getListings() {
  const res = await api.get("/listings")
  return res.data
}

export async function getZeroBid() {
  const res = await api.get("/zero-bid")
  return res.data
}

export async function getListing(id: string) {
  const res = await api.get(`/listing/${id}`)
  return res.data
}
