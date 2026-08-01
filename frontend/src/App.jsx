import { Routes, Route } from 'react-router-dom'
import Layout from './layouts/Layout'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'
export default function App() { return <Routes><Route element={<Layout />}><Route path="/" element={<Landing />} /><Route path="/dashboard" element={<Dashboard />} /></Route></Routes> }
