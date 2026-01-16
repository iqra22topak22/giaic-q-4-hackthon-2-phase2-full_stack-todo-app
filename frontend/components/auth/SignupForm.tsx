// frontend/components/auth/SignupForm.tsx
import React, { useState } from 'react';
import { FormInput as Input } from '../ui/FormInput';
import { Button } from '../ui/Button';
import { AuthenticationForm } from '../../lib/types';
import { useToast } from '../../contexts/ToastContext';

interface SignupFormProps {
  onSignup: (formData: AuthenticationForm) => void;
  loading?: boolean;
}

const SignupForm = ({ onSignup, loading = false }: SignupFormProps) => {
  const { showToast } = useToast();
  const [formData, setFormData] = useState<AuthenticationForm>({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Partial<AuthenticationForm>>({});

  const validate = (): boolean => {
    const newErrors: Partial<AuthenticationForm> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    // Clear error when user starts typing
    if (errors[name as keyof AuthenticationForm]) {
      setErrors({
        ...errors,
        [name]: undefined,
      });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validate()) {
      onSignup(formData);
    } else {
      showToast('Please fix the errors in the form', 'error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
        label="Email"
        error={errors.email}
        required
        inputSize="md"
      />

      <Input
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        placeholder="Password"
        label="Password"
        error={errors.password}
        required
        inputSize="md"
      />

      <Input
        name="confirmPassword"
        type="password"
        value={formData.confirmPassword}
        onChange={handleChange}
        placeholder="Confirm Password"
        label="Confirm Password"
        error={errors.confirmPassword}
        required
        inputSize="md"
      />

      <Button
        type="submit"
        variant="primary"
        className="w-full"
        disabled={loading}
      >
        {loading ? 'Signing up...' : 'Sign Up'}
      </Button>
    </form>
  );
};

export default SignupForm;