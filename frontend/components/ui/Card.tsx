import * as React from "react"
import { cn } from "@/lib/utils"

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "elevated" | "outlined";
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "default", ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-xl border text-card-foreground",
        {
          "bg-card shadow": variant === "default",
          "bg-card shadow-lg": variant === "elevated",
          "bg-background shadow-sm": variant === "outlined",
        },
        className
      )}
      {...props}
    />
  )
)
Card.displayName = "Card"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

export { Card, CardContent }