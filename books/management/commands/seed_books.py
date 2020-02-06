import csv

from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = "This command creates books from CSV"

    def handle(self, *args, **options):

        with open("data/BestLoanList_20200130_month.csv", encoding="euc-kr") as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for r in f_csv:
                row = r
                try:
                    Book.objects.create(
                        data=row[1],
                        author=row[2],
                        publisher=row[3],
                        pub_year=row[4],
                        volume=row[5],
                        isbn=row[6],
                        kdc=row[8],
                    )
                except Exception:
                    pass

        with open("data/BestLoanList_20200130_weekly.csv", encoding="euc-kr") as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for r in f_csv:
                row = r
                try:
                    Book.objects.create(
                        data=row[1],
                        author=row[2],
                        publisher=row[3],
                        pub_year=row[4],
                        volume=row[5],
                        isbn=row[6],
                        kdc=row[8],
                    )
                except Exception:
                    pass
        self.stdout.write(self.style.SUCCESS("Books created."))
