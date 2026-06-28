% hard3_0109  eq1=867 eq2=4632  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(f(Y,Z),f(W,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),X) = f(f(X,Z),Y) )).
