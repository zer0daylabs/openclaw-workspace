import { FC, ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  title?: string
  description?: string
  className?: string
  action?: ReactNode
}

export const Card: FC<CardProps> = ({ children, title, description, className = '', action }) => {
  return (
    <div className={`bg-white rounded-xl shadow-md border border-gray-100 ${className}`}>
      {(title || action) && (
        <div className="px-6 py-4 border-b flex justify-between items-center">
          <div>
            {title && <h3 className="text-lg font-bold text-gray-900">{title}</h3>}
            {description && <span className="text-sm text-gray-500">{description}</span>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  )
}
