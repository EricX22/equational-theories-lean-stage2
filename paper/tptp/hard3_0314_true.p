% hard3_0314  eq1=2923 eq2=1623  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(X,Z)),Y),X) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(U,X))) )).
