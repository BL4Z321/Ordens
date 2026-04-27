import csv
from django.http import HttpResponse
from django.template.loader import render_to_string
from openpyxl import Workbook
from weasyprint import HTML

class ExportacaoService:

    @staticmethod
    def exportar_csv(op, op_produtos, insumos):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachement; filename="op_{op.cod_op}_recursos.csv'

        writer = csv.writer(response)
        writer.writerow(['PRODUTOS'])
        writer.writerow(['Produto', 'Tipo', 'Tecnologia', 'Estoque', 'Qtd Necessária', 'Total', 'Status'])

        for p in op_produtos:
            writer.writerow([
                str(p.produto.modelo),
                p.produto.get_tipo_display(),
                p.produto.tecnologia,
                f'{p.produto.qtd_estoque_atual} unid.',
                f'{p.qtd_necessaria} unid.',
                f'{p.qtd_total} unid.',
                p.status_nome
            ])

        writer.writerow([])

        writer.writerow(['INSUMOS'])
        writer.writerow(['Insumo', 'Qtd Necessária', 'Estoque', 'Total Previsto', 'Status'])

        for i in insumos:
            status = 'Falta' if i.qtd_necessaria_por_unidade > i.insumo.estoque_atual else 'OK'

            writer.writerow([
                i.insumo.nome,
                f'{i.qtd_necessaria_por_unidade} {i.insumo.get_unidade_abreviada()}',
                f'{i.insumo.estoque_atual} {i.insumo.get_unidade_abreviada()}',
                f'{i.qt_total_prevista} {i.insumo.get_unidade_abreviada()}',
                status
            ])

        return response
    
    @staticmethod
    def exportar_excel(op, op_produtos, insumos):
        wb = Workbook()

        ws_prod = wb.active
        ws_prod.title = 'Produtos'

        ws_prod.append(['Produto', 'Tipo', 'Tecnologia', 'Estoque', 'Qtd Necessária', 'Total', 'Status'])

        for p in op_produtos:
            ws_prod.append([
                str(p.produto.modelo),
                p.produto.get_tipo_display(),
                p.produto.tecnologia,
                f'{p.produto.qtd_estoque_atual} unid.',
                f'{p.qtd_necessaria} unid.',
                f'{p.qtd_total} unid.',
                p.status_nome
            ])

        ws_insu  = wb.create_sheet(title='Insumos')
        ws_insu.append(['Insumo', 'Qtd Necessária', 'Estoque', 'Total Previsto', 'Status'])

        for i in insumos:
            status = 'Falta' if i.qtd_necessaria_por_unidade > i.insumo.estoque_atual else 'OK'

            ws_insu.append([
                i.insumo.nome,
                f'{i.qtd_necessaria_por_unidade} {i.insumo.get_unidade_abreviada()}',
                f'{i.insumo.estoque_atual} {i.insumo.get_unidade_abreviada()}',
                f'{i.qt_total_prevista} {i.insumo.get_unidade_abreviada()}',
                status
            ])

        response = HttpResponse(
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheettml.sheet'
        )
        response['Content-Disposition'] = f'attachement; filename="op_{op.cod_op}_recursos.xlsx"'

        wb.save(response)
        return response
    
    @staticmethod
    def gerar_pdf_ordem_producao(op, produtos, insumos):
        contexto = {
            'op': op,
            'produtos': produtos,
            'insumos': insumos
        }

        html_string = render_to_string('gestor/pdf_ordem.html', contexto)
        pdf_bytes = HTML(string=html_string).write_pdf()

        return pdf_bytes
    