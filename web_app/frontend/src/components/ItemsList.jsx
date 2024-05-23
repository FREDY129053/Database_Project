import Card from "./Card"

/* eslint-disable react/prop-types */
export default function ItemsList(props) {
	const allItems = props.items

	return (
		<>
			{!(Array.isArray(allItems) && allItems.length === 0)
				? <div className="grid grid-cols-3 gap-12">
						{allItems.map(item => {
							if (Object.hasOwn(item, 'genres')) {
								return (<Card key={Math.random()} item={item} />)
							}
						})}
					</div>
				: <p className="empty text-white font-bold tracking-wider text-2x1 leading-normal">Nothing...</p>
			}
		</>
	)
}

