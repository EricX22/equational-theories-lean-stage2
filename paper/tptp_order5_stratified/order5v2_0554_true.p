% order5v2_0554  eq1=29093 eq2=57832  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),Z),W),f(Y,U)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(f(X,X),W),X) )).
