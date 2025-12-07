"use client"
import Image from "next/image"
import { useState } from "react"

interface Props {
  src: string
  alt: string
  className?: string
}

export function ImageWithFallback({ src, alt, className }: Props) {
  const [current, setCurrent] = useState(src || "/placeholder.jpg")
  return (
    // wrapping div keeps aspect from parent; Image with fill requires position relative
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <Image
        src={current}
        alt={alt}
        fill
        className={className || "object-contain"}
        onError={() => setCurrent("/placeholder.jpg")}
      />
    </div>
  )
}

