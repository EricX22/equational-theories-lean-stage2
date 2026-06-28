% hard3_0040  eq1=215 eq2=3050  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),Y) )).
fof(goal, conjecture, ! [X] : ( X = f(f(f(f(X,X),X),X),X) )).
