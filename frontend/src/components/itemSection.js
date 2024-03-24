import React, { useState } from 'react'
import { Container, Row, Col, Carousel } from 'react-bootstrap'

const ItemSection = (props) => {
    const { item } = props
    const [photoIndex, setPhotoIndex] = useState(0)

    const handlePhotoSelect = (selectedIndex) => {
        setPhotoIndex(selectedIndex)
    }

    if (!item) { return }

    return (
        <section className="section-card">
            <Container>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Item:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {item.itemName}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Condition:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {item.condition}
                        </div>
                    </Col>
                </Row>
                {item?.itemDetails && Object.keys(item.itemDetails).map(
                    key => {
                        return (
                            <Row key={key}>
                                <Col xs={3}>
                                    <div className="card-label">
                                        {key}:
                                    </div>
                                </Col>
                                <Col>
                                    <div className="card-data">
                                        {item.itemDetails[key]}
                                    </div>
                                </Col>
                            </Row>
                        )
                    }
                )}
                {item.photos.length > 0 && (
                    <Row>
                        <Col>
                            <div className="w-30">
                            <Carousel
                                activeIndex={photoIndex}
                                onSelect={handlePhotoSelect}
                                variant="dark"
                            >
                                {item.photos.map((photo, idx) => {
                                    return (
                                        <Carousel.Item key={idx}>
                                            <div class="d-flex justify-content-center">
                                                <img
                                                    className="d-block"
                                                    src={photo.url}
                                                    alt={`Image #${idx}`}
                                                />
                                            </div>
                                            <Carousel.Caption>
                                                <h3>{photo.caption}</h3>
                                            </Carousel.Caption>
                                        </Carousel.Item>
                                    )
                                })}
                            </Carousel></div>
                        </Col>
                    </Row>
                )}

            </Container>
        </section>
    )
}

export default ItemSection