% hard3_0196  eq1=1806 eq2=545  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,X),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Z,f(X,f(Z,X)))) )).
