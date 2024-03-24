import React, { useMemo } from 'react'
import { Container, Row, Col } from 'react-bootstrap'
import { formatDate } from './utils'

const LodgingSection = (props) => {
    const { lodging } = props

    const lodgingNameLabel = useMemo(() => {
        if (lodging?.lodgingType === "hotel") {
            return "Hotel Name"
        }
        return "Lodging"
    }, [lodging])

    if (!lodging) { return }

    return (
        <section className="section-card">
            <Container>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            {lodgingNameLabel}:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {lodging.lodgingName}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Address:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {lodging.address}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Website:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {lodging.lodgingUrl}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Start Date:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {formatDate(lodging.startDate)}
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            End Date:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {formatDate(lodging.endDate)}
                        </div>
                    </Col>
                </Row>
                {lodging?.lodgingDetails && Object.keys(lodging.lodgingDetails).map(
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
                                        {lodging.lodgingDetails[key]}
                                    </div>
                                </Col>
                            </Row>
                        )
                    }
                )}
            </Container>
        </section>
    )
}

export default LodgingSection