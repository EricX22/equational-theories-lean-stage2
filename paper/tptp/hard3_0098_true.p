% hard3_0098  eq1=761 eq2=2037  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,Y),X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,X),X),f(Y,X)) )).
