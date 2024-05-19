import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'
import axios from 'axios';
import '../styles/index.css';

import noPhoto from '../styles/images/no_image.webp';

export default function Home () {
	// eslint-disable-next-line no-unused-vars
	const [publishers, setPublishers] = useState([]);
  const [filteredPublishers, setFilteredPublishers] = useState({});
	const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/game_info/publishers')
      .then(response => {
        const publishersData = response.data;
        setPublishers(publishersData);
        organizePublishers(publishersData);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

	useEffect(() => {
    const handleScroll = () => {
			console.log(window.scrollY);
      if (window.scrollY > 25) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const organizePublishers = (publishers) => {
    const organized = publishers.reduce((acc, publisher) => {
      const firstLetter = publisher.name[0].toUpperCase();
      if (firstLetter >= 'A' && firstLetter <= 'Z') {
        acc[firstLetter] = acc[firstLetter] ? [...acc[firstLetter], publisher] : [publisher];
      } else {
        acc['Other'] = acc['Other'] ? [...acc['Other'], publisher] : [publisher];
      }
      return acc;
    }, {});
    setFilteredPublishers(organized);
  };

  const scrollToSection = (letter) => {
    document.getElementById(letter).scrollIntoView({ behavior: 'smooth' });
  };

  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').concat('Other');

  return (
    <div className="app-container">
      <div className={`fixed-menu ${isScrolled ? 'scrolled' : ''}`}>
        {alphabet.map(letter => (
          <div key={Math.random()} onClick={() => scrollToSection(letter)} className="alphabet-letter">
            {letter}
          </div>
        ))}
      </div>
      <div className="content">
        {alphabet.map(letter => (
          <div key={letter} id={letter} className="section">
					<h2>{letter}</h2>
					{filteredPublishers[letter] && filteredPublishers[letter].length > 0 ? (
						<div className="publisher-grid">
							{filteredPublishers[letter].map(publisher => (
								<Link key={Math.random()} to={'/game_info/publishers/' + publisher.slug} className="publisher-card">
									<div className='info'>
										<img src={publisher.photo_url ? publisher.photo_url : noPhoto} alt={publisher.name} className="publisher-photo" />
										<div className="publisher-name">{publisher.name}</div>
									</div>
								</Link>
							))}
						</div>
					) : (
						<div className="no-publishers">No such publishers</div>
					)}
				</div>
        ))}
      </div>
    </div>
  );
	
}