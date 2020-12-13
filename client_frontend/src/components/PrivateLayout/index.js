import React from 'react';
import {Link} from 'react-router-dom';
import {Layout, Menu, Row, Col, Button} from 'antd';


export const PrivateLayout = ({children}) => {
    const {Header, Content} = Layout;

    return (
        <Layout>
            <Header className="header">
                <Row>
                    <Col span={6} className="logo">
                        <Link to='/gallery'>
                            <h2>Borovyi bachelor</h2>
                        </Link>
                    </Col>
                    <Col offset={13} span={3} className="username">
                        <p>Borovyi_Orest</p>
                    </Col>
                    <Col span={2}>
                        <Button type="primary" danger>
                            Logout
                        </Button>
                    </Col>
                </Row>
                {/*<Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']}>*/}
                {/*    <Menu.Item key="1">nav 1</Menu.Item>*/}
                {/*    <Menu.Item key="2">nav 2</Menu.Item>*/}
                {/*    <Menu.Item key="3">nav 3</Menu.Item>*/}
                {/*</Menu>*/}
            </Header>
            <Content style={{padding: '50px'}}>
                <Layout>
                    {children}
                </Layout>
            </Content>
        </Layout>
    )
};
