import React, { useMemo } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { formatDate } from './utils'
import "../style.css"

const ListingSection = (props) => {
    const { listing } = props

    const displayPrice = useMemo(() => {
        if (listing.priceCents === 0) {
            return "Free"
        }
        return (listing.priceCents / 100).toLocaleString("en-US", {
            style:"currency", currency:"USD"
        })
    }, [listing.priceCents])

    const saleButtonText = useMemo(() => {
        if (listing.saleType == "sell") { return "Buy Now" }
        if (listing.saleType == "book") { return "Book Now" }
        return "Buy Now"
    }, [listing.saleType])

    return (
        <section className="section-card">
            <h2>{listing.title}</h2>
            <div className="subheader-listing-date">
                listed {formatDate(listing.listedOn)}
            </div>
            {listing.closedOn && (
                <div className="subheader-listing-date">
                    closed {formatDate(listing.closedOn)}
                </div>
            )}

            <Container>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Status:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {listing.status}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Price:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {displayPrice}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Description:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {listing.description}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <div className="card-label">
                            <Button variant="primary">
                                {saleButtonText}
                            </Button>
                        </div>
                    </Col>
                </Row>
            </Container>
        </section>
    )
}

export default ListingSection