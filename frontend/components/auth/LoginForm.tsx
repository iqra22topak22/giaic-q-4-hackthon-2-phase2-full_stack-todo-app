// frontend/components/auth/LoginForm.tsx
import React, { useState } from 'react';
import { FormInput as Input } from '../ui/FormInput';
import { Button } from '../ui/Button';
import { useToast } from '../../contexts/ToastContext';

interface LoginFormProps {
  onLogin: (email: string, password: string) => void;
  loading?: boolean;
}

const LoginForm = ({ onLogin, loading = false }: LoginFormProps) => {
  const { showToast } = useToast();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Please fill in all fields');
      showToast('Please fill in all fields', 'error');
      return;
    }

    setError('');
    onLogin(email, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        name="email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        label="Email"
        required
        inputSize="md"
      />

      <Input
        name="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        label="Password"
        required
        inputSize="md"
      />

      {error && <p className="text-danger-500 text-sm">{error}</p>}

      <Button
        type="submit"
        variant="primary"
        className="w-full"
        disabled={loading}
      >
        {loading ? 'Signing in...' : 'Sign In'}
      </Button>
    </form>
  );
};

export default LoginForm;