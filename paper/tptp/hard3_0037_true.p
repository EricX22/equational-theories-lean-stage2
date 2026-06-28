% hard3_0037  eq1=205 eq2=3464  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(X,Y)),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(X,f(f(Y,Y),X)) )).
