#include<GL/glut.h>
#include<stdio.h>


int n;
GLfloat v[4][3] = { {0.0,0.0,1.0},{0.0,0.92,-0.33},{-0.81,-0.47,-0.33},{0.81,-0.47,-0.33} };

void myinit()
{
	glOrtho(-2.0,2.0,-2.0,2.0,-10.0,10.0);
	glClearColor(1.0,1.0,1.0,1.0);
}
void triangle(GLfloat *a, GLfloat *b, GLfloat *c)
{
	glBegin(GL_POLYGON);
	glVertex3fv(a);
	glVertex3fv(b);
	glVertex3fv(c);
	glEnd();
}

void dividetriangle(GLfloat *a, GLfloat *b, GLfloat *c, int m)
{
	GLfloat v1[3], v2[3], v3[3];
	int j;
	if (m > 0)
	{
		for (j = 0; j < 3; j++) v1[j] = (a[j] + b[j]) / 2;
		for (j = 0; j < 3; j++) v2[j] = (a[j] + c[j]) / 2;
		for (j = 0; j < 3; j++) v3[j] = (c[j] + b[j]) / 2;
		dividetriangle(a,v1,v2,m-1);
		dividetriangle(c, v2, v3, m - 1);
		dividetriangle(b, v3, v1, m - 1);
	}
	else
		triangle(a,b,c);
}

void tetrahedron(int m)
{
	glColor3f(1.0,0.0,0.0);
	dividetriangle(v[0], v[1], v[2], m);
	glColor3f(0.0, 1.0, 0.0);
	dividetriangle(v[1], v[2], v[3], m);
	glColor3f(0.0, 0.0, 1.0);
	dividetriangle(v[0], v[1], v[3], m);
	glColor3f(0.0, 0.0, 0.0);
	dividetriangle(v[0], v[2], v[3], m);
}
void display()
{
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
	tetrahedron(n);
	glFlush();
}
int main(int argc, char **argv)
{
	
	printf("Enter number of divisions");
	scanf("%d",&n);
	glutInit(&argc, argv);
	//glutInitWindowPosition(0, 0);
	glutInitWindowSize(500, 500);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB|GLUT_DEPTH);
	glutCreateWindow("3D Gasket");
	//	gluOrtho2d(0.0,800.0,0.0,600.0);
	glutDisplayFunc(display);
	myinit();
	glEnable(GL_DEPTH_TEST);
	glutMainLoop();
}




