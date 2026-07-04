% order5v2_1281  eq1=30457 eq2=17320  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(f(Z,W),X))),Y) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(W,f(W,U)))) )).
