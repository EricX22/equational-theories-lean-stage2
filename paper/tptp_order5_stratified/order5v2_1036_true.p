% order5v2_1036  eq1=17322 eq2=42838  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(W,f(U,Y)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(Y,f(Z,f(f(X,Y),X))) )).
