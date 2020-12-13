import React, {Component} from 'react';
import {PrivateLayout} from '../../PrivateLayout'
import {RawImageTabContainer} from '../../../containers/client/RawImageTabContainer'
import {TransformedImageTabContainer} from '../../../containers/client/TransformedImageTabContainer'
import {Row, Col, Tabs, message, Upload, Button, Modal, Input} from 'antd';
import {LoadingOutlined, PlusOutlined} from '@ant-design/icons';
import imageUrl from '../../../photo_2020-05-23_17-28-32.jpg'

const {TabPane} = Tabs;


export class GalleryPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            imageUrl: imageUrl,
            loading: false,
            modalVisible: false,
        }
    }

    getBase64(img, callback) {
        const reader = new FileReader();
        reader.addEventListener('load', () => callback(reader.result));
        reader.readAsDataURL(img);
    }

    handleChange = info => {
        if (info.file.status === 'uploading') {
            this.setState({loading: true});
            return;
        }
        if (info.file.status === 'done') {
            // Get this url from response in real world.
            this.getBase64(info.file.originFileObj, imageUrl =>
                this.setState({
                    imageUrl,
                    loading: false,
                }),
            );
        }
    };

    beforeUpload(file) {
        const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
        if (!isJpgOrPng) {
            message.error('You can only upload JPG/PNG file!');
        }
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isLt2M) {
            message.error('Image must smaller than 2MB!');
        }
        return isJpgOrPng && isLt2M;
    }

    setModalVisible(modalVisible) {
        this.setState({modalVisible});
    }

    render() {
        const {imageUrl, modalVisible, loading} = this.state;

        const uploadButton = (
            <div>
                {loading ? <LoadingOutlined/> : <PlusOutlined/>}
                <div className="ant-upload-text">Upload</div>
            </div>
        );
        return (
            <PrivateLayout>
                <Row>
                    <Col offset={20} span={4}>
                        <Button
                            type="primary"
                            onClick={() => this.setModalVisible(true)}
                        >
                            Upload image
                        </Button>
                    </Col>
                </Row>

                <Modal
                    title="Upload image"
                    centered
                    visible={modalVisible}
                    onOk={() => this.setModalVisible(false)}
                    onCancel={() => this.setModalVisible(false)}
                >
                    <Row>
                        <Col offset={5}>
                            <Upload
                                name="avatar"
                                listType="picture-card"
                                className="avatar-uploader"
                                showUploadList={false}
                                beforeUpload={this.beforeUpload}
                                onChange={this.handleChange}
                            >
                                {imageUrl ? <img src={imageUrl} alt="avatar" style={{width: '100%'}}/> : uploadButton}
                            </Upload>
                        </Col>
                    </Row>
                    <Input placeholder="Enter image name for gallery"/>
                </Modal>
                <div className="card-container">
                    <Tabs type="card">
                        <TabPane tab="Raw images" key="1">
                            <RawImageTabContainer/>
                        </TabPane>
                        <TabPane tab="Transformed images" key="2">
                            <TransformedImageTabContainer/>
                        </TabPane>
                    </Tabs>
                </div>
            </PrivateLayout>
        );
    }
};
