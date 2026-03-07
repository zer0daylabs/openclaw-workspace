import { FC, ComponentProps } from 'react'

interface InputProps extends Omit<ComponentProps<'input'>, 'size'> {
  label?: string
  error?: string
  helperText?: string
}

export const Input: FC<InputProps> = ({ label, error, helperText, className = '', id, ...props }) => {
  return (
    <div className={className}>
      {label && <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-2">{label}</label>}
      <input
        id={id}
        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
        {...props}
      />
      {error && <span className="text-red-600 text-sm mt-1 block">{error}</span>}
      {helperText && !error && <span className="text-gray-500 text-sm mt-1 block">{helperText}</span>}
    </div>
  )
}
