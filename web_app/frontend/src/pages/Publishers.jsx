import { useEffect, useState } from 'react';
import { Spin } from 'antd';
import axios from 'axios';
import '../index.css';
import ItemsList from '../components/ItemsList';

export default function Home () {
	const [allPublishers, setAllPublishers] = useState([])

	const getAllPublishers = () => {
		axios.get('http://127.0.0.1:8000/game_info/publishers').then(resp => {
			setAllPublishers(resp.data)
		})
	}

	useEffect(() => {
		getAllPublishers()
	}, [])

	return (
		<>
			{allPublishers ? <ItemsList items={allPublishers} /> : <Spin size='large' />}
		</>
	)
	
}