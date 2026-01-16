import * as React from "react";
import { Input as BaseInput } from "./Input";
import { cn } from "@/lib/utils";

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  inputSize?: 'sm' | 'md' | 'lg';
}

const FormInput = React.forwardRef<HTMLInputElement, FormInputProps>(
  ({ label, error, inputSize = 'md', className, ...props }, ref) => {
    const sizeClasses = {
      sm: "py-1 px-2 text-sm",
      md: "py-2 px-3 text-base",
      lg: "py-3 px-4 text-lg"
    };

    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            {label}
          </label>
        )}
        <BaseInput
          ref={ref}
          className={cn(
            sizeClasses[inputSize],
            error && "border-red-500 focus:ring-red-500 focus:border-red-500",
            className
          )}
          {...props}
        />
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      </div>
    );
  }
);

FormInput.displayName = "FormInput";

export { FormInput };