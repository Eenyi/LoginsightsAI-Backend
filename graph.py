import matplotlib
import matplotlib.pyplot as plt
import io
matplotlib.use('Agg')
class Graph:
    @staticmethod
    def generate_graph(data, labels = None, graph_type = 'line', title = "Graph"):
        fig, ax = plt.subplots()
        if graph_type == 'line':
            ax.plot(data, label=labels)
        elif graph_type == 'bar':
            ax.bar(range(len(data)), data, tick_label=labels)
            plt.xticks(rotation=45)
        elif graph_type == 'scatter':
            ax.scatter(range(len(data)), data, label=labels)
        elif graph_type == 'pie':
            if labels:
                ax.pie(data, labels=labels, autopct='%1.1f%%')
            else:
                ax.pie(data, autopct='%1.1f%%')
        else:
            return
        
        if title:
            plt.title(title)
        if labels  and graph_type != 'pie' and graph_type != "bar":
            ax.legend()
        
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        return buf