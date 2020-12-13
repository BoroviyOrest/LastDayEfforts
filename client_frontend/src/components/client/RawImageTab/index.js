import React from 'react';
import _ from 'lodash';
import {Card, Col, Row, Empty} from 'antd';

const {Meta} = Card;

export const RawImageTab = ({imageList, onCardClick}) => {
    let rawImagesContent;

    if (_.isEmpty(imageList)) {
        rawImagesContent = (
            <Col span={24}>
                <Empty/>
            </Col>
        );
    } else {
        rawImagesContent = _.map(imageList, (image) => {
            const {name, createdOn, imageUrl, id} = image;
            const description = `Created on ${createdOn}`;
            return (
                <Col span={6} style={{marginBottom: '16px'}}>
                    <Card
                        hoverable
                        cover={<img alt={name} src={imageUrl}/>}
                        onClick={() => onCardClick(id)}
                    >
                        <Meta title={name} description={description}/>
                    </Card>
                </Col>
            )
        });
    }

    return (
        <Row gutter={16}>
            {rawImagesContent}
        </Row>
    )
};
