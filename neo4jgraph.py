from py2neo import Graph, Node, Relationship, NodeMatcher
import csv
# node

# 电影名
movie_name_list = ['movie_name_list']
# 主演
actor_name_list = ['actor_name_list']
# 导演
director_name_list = ['derector_name_list']

# label
movie_name_label = '电影名'
actor_name_label = '主演'
director_name_label = '导演'
main_node_label = '豆瓣电影知识图谱'

class neoGraph():
    def __init__(self):
    # 连接数据库
        self.graph = Graph("http://localhost:7474", username="neo4j", password='1')
        self.data_message_list = []

    def read_data(self):
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.data_message_list = list(reader)


    def create_node(self):
        # 创建主节点
        main_node = Node(main_node_label, name=main_node_label)
        self.graph.create(main_node)
        i = 1
        for each_message in self.data_message_list:
            # 创建节点
            movie_node = Node(movie_name_label, name=each_message[0])
            self.graph.create(movie_node)
            actor_node = Node(actor_name_label, name=each_message[-1])
            self.graph.create(actor_node)
            direct_node = Node(director_name_label, name=each_message[1])
            self.graph.create(direct_node)
            # 创建关系
            print('no.')
            print(i)
            movie_to_main = Relationship(movie_node, 'no.'+str(i), main_node)
            i += 1

            self.graph.create(movie_to_main)
            actor_to_movie = Relationship(actor_node, '一句话电影', movie_node)
            self.graph.create(actor_to_movie)
            direct_to_movie = Relationship(direct_node, '导演', movie_node)
            self.graph.create(direct_to_movie)


    def create_rel(self):
        matcher = NodeMatcher(self.graph)
        main_node = matcher.match(main_node_label, name=main_node_label)
        # 建立主节点和电影名的联系
        i = 1
        for each_movie in movie_name_list:
            movie_node = matcher.match(movie_name_label, name=each_movie)
            movie_to_main = Relationship(movie_node, 'no.' + str(i), main_node)
            i += 1
            self.graph.create(movie_to_main)
        # 建立导演和电影名的联系

        # 建立主演和电影名的联系

    def clean_node(self):
        # 清空数据库
        self.graph.delete_all()


if __name__ == '__main__':
    c = neoGraph()
    c.clean_node()
    c.read_data()
    c.create_node()