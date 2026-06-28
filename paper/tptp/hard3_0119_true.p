% hard3_0119  eq1=977 eq2=1231  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(X,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(f(X,Y),Y),X)) )).
