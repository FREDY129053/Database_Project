// import { useEffect, useState } from 'react';
// import { Spin } from 'antd';
// import axios from 'axios';
import './index.css';
// import ItemsList from './components/ItemsList';
import Navbar from './components/Navbar';
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home';
import Publishers from './pages/Publishers'
import GameInfo from './pages/GameInfo';

function App() {
	// const [allGames, setAllGames] = useState([])

	// const getAllGames = () => {
	// 	axios.get('http://127.0.0.1:8000/game_info').then(resp => {
	// 		setAllGames(resp.data)
	// 	})
	// }

	// useEffect(() => {
	// 	getAllGames()
	// }, [])

  return (
    <>
			<Navbar />
      <div className='mx-auto my-auto'>
				<Routes>
					<Route path='/' element={<Home />} />
					<Route path='/game_info' element={<Home />} />
					<Route path='/game_info/publishers' element={<Publishers />} />
					<Route path='/game_info/:slug' element={<GameInfo />} />
				</Routes>
				{/* {allGames ? <ItemsList items={allGames} /> : <Spin size='large' />} */}
			</div>
			
    </>
  )
}

export default App
