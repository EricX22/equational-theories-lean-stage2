% order5_0037  eq1=39449 eq2=5996  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(X,Z)),W),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(Y,f(f(Z,W),Y)))) )).
