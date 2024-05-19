/* eslint-disable react/prop-types */
import { useState } from "react"

export default function Pagination({data, RenderComponent, pageLimit, dataLimit}) {
	const [pages] = useState(Math.round(data.lenght / dataLimit))
	const [currPage, setCurrPage] = useState(1)

	return (
		<>Helloo</>
	)
}