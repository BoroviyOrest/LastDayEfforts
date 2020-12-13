import React from 'react';
import _ from 'lodash';
import {Card, Col, Row, Empty, Modal, Button, Spin} from 'antd';
import {DownloadOutlined} from '@ant-design/icons';

const {Meta} = Card;

export const TransformedImageTab = ({imageList, isModalOpen, closeModal, openModal, modalImage}) => {
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
                        style={{height: '300px'}}
                        cover={
                            <div className="example">
                                <Spin/>
                            </div>}
                        onClick={() => openModal(id)}
                    >
                        <Meta title={name} description={description}/>
                    </Card>
                </Col>
            )
        });
    }
    console.log(modalImage);
    return (
        <Row gutter={16}>
            {rawImagesContent}
            <Modal
                title={modalImage.name}
                centered
                visible={isModalOpen}
                onOk={closeModal}
                onCancel={closeModal}
                footer={[
                    <Button>
                        <DownloadOutlined/> Click to Download
                    </Button>
                ]}
            >
                <img
                    alt={modalImage.id}
                    src={modalImage.imageUrl}
                    className='modal_image'
                />
            </Modal>
        </Row>
    )
};
