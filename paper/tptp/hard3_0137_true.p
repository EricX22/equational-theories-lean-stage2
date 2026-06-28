% hard3_0137  eq1=1065 eq2=1647  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Z)),Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,Y),f(f(X,Y),X)) )).
