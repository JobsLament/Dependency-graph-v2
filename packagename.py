import gzip
import os
import networkx as nx
import subprocess
import sys

def extract_gz_file(archive_path):
    """
    Если это текстовый файл, просто читаем его.
    """
    with gzip.open(archive_path, 'rt', encoding='utf-8') as f:
        content = f.read()
    return content

def parse_dependencies(content):
    """
    Извлекаем зависимости из распакованного содержимого.
    Предполагается, что файл содержит блоки с данными о каждом пакете.
    """
    dependencies = {}
    packages = content.split("\n\n")
    
    for package in packages:
        lines = package.splitlines()
        package_name = None
        package_deps = []
        
        for line in lines:
            if line.startswith("Package:"):
                package_name = line.split(":", 1)[1].strip()
            elif line.startswith("Depends:"):
                depends = line.split(":", 1)[1].strip()
                package_deps = [dep.split()[0].strip() for dep in depends.split(",")]
        
        if package_name:
            dependencies[package_name] = package_deps
    
    return dependencies

def build_dependency_graph(dependencies, root_package):
    """
    Строит граф зависимостей для заданного пакета и его зависимостей.
    """
    G = nx.DiGraph()
    
    def add_dependencies(package):
        if package in dependencies:
            for dep in dependencies[package]:
                G.add_edge(package, dep)
                if dep not in G:
                    add_dependencies(dep)

    add_dependencies(root_package)
    return G

def save_graph_as_png(G, output_file):
    """
    Сохраняем граф в формате PNG с использованием Graphviz.
    """
    dot_string = nx.nx_agraph.to_agraph(G).to_string()
    dot_file = 'dependency_graph.dot'
    
    with open(dot_file, 'w') as f:
        f.write(dot_string)
    
    try:
        subprocess.run(['dot', '-Tpng', '-Gdpi=300', '-Gnodesep=0.1', '-Gsize=10,10', '-Grankdir=LR', '-Gfontname=Helvetica', dot_file, '-o', output_file], check=True)
        print(f"Граф зависимостей успешно сохранен в файл {output_file}")
    except subprocess.CalledProcessError:
        print(f"Ошибка при рендеринге графа в {output_file}. Убедитесь, что Graphviz установлен.")

def main(archive_path, output_file, root_package):
    content = extract_gz_file(archive_path)
    
    dependencies = parse_dependencies(content)
    
    if root_package not in dependencies:
        print(f"Пакет {root_package} не найден в архиве.")
        sys.exit(1)
    
    G = build_dependency_graph(dependencies, root_package)
    
    save_graph_as_png(G, output_file)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Использование: python visualizer.py <путь_к_Packages.gz> <выходной_файл.png> <имя_пакета>")
        sys.exit(1)
    
    archive_path = sys.argv[1]
    output_file = sys.argv[2]
    root_package = sys.argv[3]