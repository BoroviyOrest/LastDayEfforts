import React from 'react';
import _ from 'lodash';
import {Layout, Menu, Empty, Card, Row, Col, Typography, Slider, Button} from 'antd';
import {PrivateLayout} from "../../PrivateLayout";

const {Content, Sider} = Layout;
const {Meta} = Card;
const {Title} = Typography;

export const RawImagePage = ({image, stylesList, name, description}) => {
    let stylesContent;

    if (_.isEmpty(stylesList)) {
        stylesContent = (
            <Empty/>
        );
    } else {
        stylesContent = _.map(stylesList, (style) => {
            const {description, id} = style;
            return (
                <Menu.Item key={id}>{description}</Menu.Item>
            )
        });
    }
    return (
        <PrivateLayout>
            <Content style={{padding: '24px', background: '#fff'}}>
                <Row>
                    <Col span={10}>
                        <Card
                            style={{width: '100%'}}
                            cover={
                                <img alt={name} src={image}/>
                            }
                        >
                            <Meta
                                title={name}
                                description={description}
                            />
                        </Card>
                    </Col>
                    <Col span={14} style={{padding: '0 24px'}}>
                        <Title>Raw image transformation</Title>
                        <p>Please, select style and quality to proceed image</p>
                        <Slider
                            defaultValue={1}
                            max={2}
                            marks={{0: 'Low', 1: 'Medium', 2: 'High'}}
                        />
                        <Button type="primary" size='large' style={{float: 'right', marginTop: '50px'}}>
                            Transform
                        </Button>
                    </Col>
                </Row>
            </Content>
            <Sider width={200} style={{borderLeft: '1px solid #f0f2f5'}}>
                <Menu
                    mode="inline"
                    defaultSelectedKeys={['1']}
                    style={{height: '100%'}}
                >
                    {stylesContent}
                </Menu>
            </Sider>
        </PrivateLayout>
    )
};
