import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'

const SourceItemSection = (props) => {
    const { sourceItem } = props

    if (!sourceItem) { return }

    return (
        <section className="section-card">
            <Container>
                <Row>
                    <Col xs={3}>
                        <div className="card-label">
                            Source:
                        </div>
                    </Col>
                    <Col>
                        <div className="card-data">
                            {sourceItem.sourceItemName}
                        </div>
                    </Col>
                </Row>
                {sourceItem?.sourceItemDetails && Object.keys(sourceItem.sourceItemDetails).map(
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
                                        {sourceItem.sourceItemDetails[key]}
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

export default SourceItemSection