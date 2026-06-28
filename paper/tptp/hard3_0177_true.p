% hard3_0177  eq1=1573 eq2=3068  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(Y,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(f(X,Y),X),Y),X) )).
