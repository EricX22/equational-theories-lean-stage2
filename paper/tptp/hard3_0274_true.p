% hard3_0274  eq1=2645 eq2=2287  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,X),f(X,X)),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(Z,W))),Z) )).
