import './styles/index.css';
import Navbar from './components/Navbar';
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home';
import Publishers from './pages/Publishers'
import GameInfo from './pages/GameInfo';
import PublisherInfo from './pages/PublisherInfo';

function App() {
  return (
    <>
			<Navbar />
      <div className='mx-auto my-auto'>
				<Routes>
					<Route path='/' element={<Home />} />
					<Route path='/game_info' element={<Home />} />
					<Route path='/game_info/publishers' element={<Publishers />} />
					<Route path='/game_info/:slug' element={<GameInfo />} />
					<Route path='/game_info/publishers/:slug' element={<PublisherInfo />} />
				</Routes>
			</div>
    </>
  )
}

export default App
