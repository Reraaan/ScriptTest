// ��������I/O�⣬����ʹ����һ�����������ʽ
#include <stdio.h>
#include <iostream>
#include <iomanip>
using namespace std;

// ����printMonth����Ҫ��ĸ�ʽ��ӡĳ��ĳ�µ�����
// ������year-�꣬month-��
// ����ֵ����
void printMonth(int year, int month);

// leapYear���ж�����
// ������y-��
// ����ֵ��1-�����꣬0-��������
int leapYear(int y)
{
    if(y % 4 == 0 && y % 100 != 0 || y % 400 == 0)
        return 1;
    return 0;
}

// ����whatDay:����ĳ��ĳ�µ�1�������ڼ�
// ������year-�꣬month-��
// ����ֵ��1��7--����1��������
int whatDay(int year, int month)
{
    // 1������������һ
    int w = 1;
    int i;

    // 1��year-1����ȫ��
    for(i = 1; i < year; i++)
    {
        if(leapYear(i))
            w += 366;
        else
            w += 365;
    }
    switch(month)
    {
    case 12: // ���µ�
        w += 30;
    case 11: // ���µ�
        w += 31;
    case 10: // ���µ�
        w += 30;
    case 9:  // ���µ�
        w += 31;
    case 8:  // ���µ�
        w += 31;
    case 7:  // ���µ�
        w += 30;
    case 6:  // ���µ�
        w += 31;
    case 5:  // ���µ�
        w += 30;
    case 4:  // ���µ�
        w += 31;
    case 3:  // ���µ�
        if(leapYear(year))
            w += 29;
        else
            w += 28;
    case 2:  // ���µ���
        w += 31;
    case 1:  // 1�²�����
        ;
    }

    // �õ�-6������Ϊ������
    w = w % 7;

    // ����������
    if(w == 0)
        w = 7;
    return w;
}

// �������油����룬ʵ�ֺ���printMonth
/*************** Begin **************/
void printMonth(int year, int month)
{
	cout<<"  һ  ��  ��  ��  ��  ��  ��"<<endl;
	
	int k=whatDay(year,month);
	
	for(int i=1; i<=k-1; i++)
		cout<<"    ";
		
	int t=k-1;
	int w;
	switch(month)
	{
		case 12:
			w=31;
				break;
		case 11:
			w=30;
				break;
		case 10:
			w=31;
				break;
		case 9:
			w=30;
				break;
		case 8:
			w=31;
				break;
		case 7:
			w=31;
				break;
		case 6:
			w=30;
				break;
		case 5:
			w=31;
				break;
		case 4:
			w=30;
				break;
		case 3:
			w=31;
				break;
		case 2:
			if(leapYear(year))
				w=29;
			else
				w=28;
				break;
		case 1:
			w=31;
				break;
	}
	
	for(int i=1; i<=w; i++)
	{
		cout<<setw(4)<<i;
		t++;
		if(t==7)
		{
			cout<<endl;
			t=0;
		}
	}
}

/*************** End **************/

int main()
{
    // �ꡢ��
    int y, m;

    // ��������
    cin >> y >> m;

    // ��������µ�����
    printMonth(y,m);

    return 0;
}
