% order5_0190  eq1=43581 eq2=51838  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(Z,Y),f(Y,X))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),f(X,X)),W) )).
