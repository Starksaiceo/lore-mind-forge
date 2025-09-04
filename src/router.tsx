import { createBrowserRouter } from 'react-router-dom';
import LandingPage from './pages/Landing';
import PricingPage from './pages/Pricing';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Voice from './pages/Voice';
import Products from './pages/Products';
import Billing from './pages/Billing';
import Activity from './pages/Activity';
import Operations from './pages/Operations';
import AdminDashboard from './pages/AdminDashboard';
import AdminUsers from './pages/AdminUsers';
import AdminSystem from './pages/AdminSystem';
import NotFound from './pages/NotFound';
import Guard from './components/Guard';

export const router = createBrowserRouter([
  // Public routes
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/pricing',
    element: <PricingPage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
  // Protected user routes
  {
    path: '/dashboard',
    element: (
      <Guard role="user">
        <Dashboard />
      </Guard>
    ),
  },
  {
    path: '/chat',
    element: (
      <Guard role="user">
        <Chat />
      </Guard>
    ),
  },
  {
    path: '/voice',
    element: (
      <Guard role="user">
        <Voice />
      </Guard>
    ),
  },
  {
    path: '/products',
    element: (
      <Guard role="user">
        <Products />
      </Guard>
    ),
  },
  {
    path: '/billing',
    element: (
      <Guard role="user">
        <Billing />
      </Guard>
    ),
  },
  {
    path: '/activity',
    element: (
      <Guard role="user">
        <Activity />
      </Guard>
    ),
  },
  {
    path: '/operations',
    element: (
      <Guard role="user">
        <Operations />
      </Guard>
    ),
  },
  // Admin routes
  {
    path: '/admin',
    element: (
      <Guard role="admin">
        <AdminDashboard />
      </Guard>
    ),
  },
  {
    path: '/admin/users',
    element: (
      <Guard role="admin">
        <AdminUsers />
      </Guard>
    ),
  },
  {
    path: '/admin/system',
    element: (
      <Guard role="admin">
        <AdminSystem />
      </Guard>
    ),
  },
  // 404
  {
    path: '*',
    element: <NotFound />,
  },
]);