% order5_0060  eq1=38080 eq2=51172  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(f(Y,X),X)),Z),Y) )).
fof(goal, conjecture, ! [U,V,W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(W,U),V)),W) )).
